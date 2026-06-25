/**
 * A native JavaScript implementation of the Archipelago Network Protocol.
 */
class ArchipelagoClient {
  constructor({ hostname, port, game, playerName, password = "" }) {
    this.url = `ws://${hostname}:${port}`
    this.game = game
    this.playerName = playerName
    this.password = password
    this.socket = null
    this.lastProcessedIndex = 0 // Tracks received items to maintain sync
  }

  /**
   * Establishes the WebSocket connection.
   */
  connect() {
    // Note: If running in Node.js, require the 'ws' package: const WebSocket = require('ws');
    this.socket = new WebSocket(this.url)

    this.socket.onopen = () => {
      console.log(
        "WebSocket connection established. Awaiting 'RoomInfo' from server...",
      )
    }

    this.socket.onmessage = (event) => {
      try {
        // Archipelago always wraps commands inside a JSON list
        const packets = JSON.parse(event.data)
        for (const packet of packets) {
          this.handlePacket(packet)
        }
      } catch (err) {
        console.error("Failed to parse incoming JSON payload:", err)
      }
    }

    this.socket.onclose = (event) => {
      console.log(
        `Disconnected from Archipelago server. Code: ${event.code}`,
      )
    }

    this.socket.onerror = (error) => {
      console.error("WebSocket network error:", error)
    }
  }

  /**
   * Standardized helper to transmit packets to the server.
   */
  sendPackets(packetsArray) {
    console.log("SENDING TO SERVER:", JSON.stringify(packetsArray)) // <-- Add this line
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(packetsArray))
    } else {
      console.error(
        "Cannot send packet; WebSocket connection is closed.",
      )
    }
  }

  /**
   * Routes inbound packets to their respective protocol handlers based on 'cmd'
   */
  handlePacket(packet) {
    switch (packet.cmd) {
      case "RoomInfo":
        this.onRoomInfo(packet)
        break
      case "Connected":
        this.onConnected(packet)
        break
      case "ConnectionRefused":
        this.onConnectionRefused(packet)
        break
      case "ReceivedItems":
        this.onReceivedItems(packet)
        break
      case "PrintJSON":
        this.onPrintJSON(packet)
        break
      case "RoomUpdate":
        this.onRoomUpdate(packet)
        break
      case "InvalidPacket":
        console.error("❌ Archipelago Server rejected payload:", {
          type: packet.type,
          reason: packet.text,
          originalCommand: packet.original_cmd,
        })
        break
      default:
        console.log(
          `Received unhandled protocol command: ${packet.cmd}`,
        )
    }
  }
  onRoomUpdate(packet) {
    console.log("[Archipelago] Room state updated by server.")

    // If other locations were checked (e.g. by a co-op partner in your slot)
    if (packet.checked_locations) {
      if (!this.checkedLocations) this.checkedLocations = []

      packet.checked_locations.forEach((loc) => {
        if (!this.checkedLocations.includes(loc)) {
          this.checkedLocations.push(loc)
        }
        // Remove from missing locations list if it's there
        if (this.missingLocations) {
          this.missingLocations = this.missingLocations.filter(
            (m) => m !== loc,
          )
        }
      })
    }
  }
  /**
   * Handshake Step 2: Server sends RoomInfo.
   * Handshake Step 5: Client replies with authentication credentials (Connect).
   */
  onRoomInfo(packet) {
    console.log(
      `RoomInfo received. Multiworld Seed: ${packet.seed_name}`,
    )

    // const connectPayload = {
    //   cmd: "Connect",
    //   password: this.password,
    //   game: this.game,
    //   name: this.playerName,
    //   uuid: this.generateUUID(),
    //   version: { major: 0, minor: 6, build: 2, class: "Version" },
    //   // items_handling configuration:
    //   // 7 (0b111) = Receive items from other worlds, own world, and starting inventory.
    //   items_handling: 7,
    //   tags: ["Tracker"], // Capabilities list (e.g., "Tracker", "TextOnly")
    //   slot_data: true,
    // }
    const connectPayload = {
      cmd: "Connect",
      password: this.password,
      game: this.game,
      name: this.playerName,
      uuid: this.generateUUID(),
      version: { major: 0, minor: 6, build: 2, class: "Version" },
      items_handling: 7,
      tags: [], // 🔑 Change this to an empty array (or ["TextOnly"])
      slot_data: true,
    }

    console.log("Authenticating with server...")
    this.sendPackets([connectPayload])
  }

  /**
   * Handshake Step 6 (Success): Server accepts client authentication.
   */
  onConnected(packet) {
    console.log(
      `Successfully connected! Team: ${packet.team}, Slot ID: ${packet.slot}`,
    )

    // 1. Mark the client as ready for gameplay packets
    this.isAuthenticated = true

    this.team = packet.team
    this.slot = packet.slot
    this.missingLocations = packet.missing_locations
    this.checkedLocations = packet.checked_locations
  }

  /**
   * Handshake Step 6 (Failure): Server rejects connection credentials.
   */
  onConnectionRefused(packet) {
    console.error(
      "Authentication rejected by server. Errors:",
      packet.errors,
    )
  }

  /**
   * Handshake Step 7 / Syncing: Server delivers items assigned to this player.
   */
  onReceivedItems(packet) {
    console.log(
      `Received packet containing ${packet.items.length} items.`,
    )

    // Index 0 requires erasing prior inventory state and accepting this list fresh.
    if (packet.index === 0) {
      console.log("Resetting local inventory tracking.")
    }

    packet.items.forEach((item, offset) => {
      const globalIndex = packet.index + offset
      console.log(
        `[Item Received] ID: ${item.item} at Location: ${item.location} from Player Slot: ${item.player}`,
      )
      this.lastProcessedIndex = globalIndex + 1
    })
  }

  /**
   * Handshake Step 8 / Live Chat: Displays broad multiworld chat notifications.
   */
  onPrintJSON(packet) {
    // Combine text parts into a single string
    const messageText = packet.data
      .map((part) => part.text || "")
      .join("")
    console.log(`[Archipelago] ${messageText}`)
  }

  /**
   * Application Action: Send items checked inside the game client to the multiworld server.
   */
  sendLocationChecks(locationIds) {
    if (!this.isAuthenticated) {
      console.error(
        "Cannot send checks yet. Waiting for server authentication handshake to complete.",
      )
      return
    }
    const checkPayload = {
      cmd: "LocationChecks",
      locations: locationIds, // Array of integer location IDs
    }
    this.sendPackets([checkPayload])
  }

  generateUUID() {
    return Math.random().toString(36).substring(2, 15)
  }
}
