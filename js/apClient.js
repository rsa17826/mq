/**
 * @typedef {Object} ItemNameToId
 * @property {Record<string,string>} Archipelago
 * @property {Record<string,string>} MathQuest
 * @property {Record<string, string>} [key]
 */

/**
 * @typedef {Object} LocationIdToName
 * @property {Record<string,string>} Archipelago
 * @property {Record<string,string>} MathQuest
 * @property {Record<string,string>} [key]
 */

/**
 * @typedef {Object} ScoutedItems
 * @property {string} itemName
 * @property {number} itemPlayer
 * @property {string} locationName
 * @property {number} flags
 */

const itemColors = {
  food: "green",
  item: "brown",
  loot: "brown",
  filler: "brown",
  misc: "pink",
  skill: "yellow",
  quest: "yellow",
  craft: "orange",
  trap: "red",
  magic: "purple",
  weapon: "darkgrey",
  armor: "grey",
  permit: "darkorange",
}

function highlightArray(str) {
  // Updated regex to match brackets, commas with spaces,
  // or strings while avoiding apostrophes inside words (\w'\w)
  const regex = /\[|\]|,\s*|'([^'\\]*(?:\\.[^'\\]*)*)'(?!\s*\w)/g

  return str.replace(regex, (match, innerGroup) => {
    if (match === "[" || match === "]") {
      return `@purple!${match}@!`
    } else if (innerGroup !== undefined) {
      // It's a valid string literal inside the array
      return `@blue!"@!@green!${innerGroup}@!@blue!"@!`
    } else {
      // It's a comma (and optional whitespace)
      return `@blue!${match}@!`
    }
  })
}
/**
 * @typedef {Object} Packet
 * @property {string} cmd
 * @property {any?} [type]
 * @property {string?} [text]
 * @property {string?} [original_cmd]
 * @property {string?} [seed_name]
 * @property {string?} [games]
 * @property {string?} [errors]
 * @property {string[]?} [tags]
 * @property {number[]?} [checked_locations]
 * @property {{games:{location_name_to_id:string},time:any, cause:string|undefined, source:string, coloredCause:string|undefined}?} [data]
 */

/**
 * @param {string} str
 */
function removeColors(str) {
  return str.replace(/@console!.*?@!/g, "").replace(/@[a-z]*!/g, "")
}

/**
 * @param {{itemName:string,itemPlayer:number}} data
 * @param {boolean} useColor
 * @returns {string}
 */
function formatItemName(data, useColor) {
  var owner =
    data.itemPlayer != -1 ?
      `${data.itemPlayer == ap.slot ? "@pink!your" : `@pink!${ap.slotInfo[data.itemPlayer].name}'s`}@!`
    : ""
  if (data.itemName.includes(":")) {
    var name = data.itemName.split(":")
    name[1] ??= name[0]
    var color = itemColors[name[0]]
    if (name[0] == "permit") {
      name[1] += " permit"
      name[0] = ""
    } else if (name[0] == "skill") {
      name[1] += " skill"
      name[0] = ""
    } else if (name[0] == "magic") {
      name[1] += " spell"
      name[0] = ""
    } else if (name[0] == "quest") {
      name[1] += " quest"
      name[0] = ""
    }
    if (name[1].includes(".") && name[0] != "quest") {
      name[1] = "progressive " + name[1].split(".")[0]
    }
    // @ts-ignore
    name = `${owner ? owner + " " : ""}${`@${color}!@console!${data.itemName} - @!@${color}!${name[1]}@!`}`
  } else {
    // @ts-ignore
    var name = `${owner ? owner + " " : ""}@green!${name}@!`
  }
  // @ts-ignore
  return !useColor ? removeColors(name) : name
}

/**
 * A native JavaScript implementation of the Archipelago Network Protocol.
 */
class ArchipelagoClient {
  /**
   *
   * @param {{hostname:string,port:number,game:string,playerName:string,password: string}} param0
   */
  constructor({ hostname, port, game, playerName, password = "" }) {
    this.url = `wss://${hostname}:${port}`
    this.game = game
    this.hostname = hostname
    this.port = port
    this.playerName = playerName
    this.password = password
    /** @type {WebSocket} */
    this.socket
    this.lastProcessedIndex = 0 // Tracks received items to maintain sync
    this.itemCount = 0 // Tracks received items to maintain sync
    /** @type {ItemNameToId} */
    // @ts-ignore
    this.itemIdToName = {}
    /** @type {LocationIdToName} */
    // @ts-ignore
    this.locationIdToName = {}
    /** @type {number[]} */
    this.missingLocations
    /** @type {number[]} */
    this.checkedLocations
    /** @type {Object.<string, ScoutedItems>} */
    this.scoutedItems = {}
    this.deathLinkEnabled = true
    this.isFallbackMode = false
    this.doneConnecting = false
    // Look for a saved preference for this specific host
    this.storageKey = `apUseWss - ${hostname}:${port}`
    this.wss = localStorage[this.storageKey] !== "false"

    this.url =
      this.wss ?
        `wss://${hostname}:${port}`
      : `ws://${hostname}:${port}`
    window.onApCreated.forEach((e) => e(this))
  }
  /**
   * Establishes the WebSocket connection.
   */
  connect() {
    // apLog(this.url)
    this.socket = new WebSocket(this.url)

    this.socket.onopen = () => {
      apLog(
        `WebSocket connection established (${this.url.split(":")[0]}). Awaiting '@green!RoomInfo@!' from server...`,
      )
    }

    this.socket.onmessage = (event) => {
      try {
        const packets = JSON.parse(event.data)
        for (const packet of packets) {
          this.handlePacket(packet)
        }
      } catch (err) {
        apError("Failed to parse incoming JSON payload:", err)
      }
    }

    this.socket.onclose = (event) => {
      apWarn(
        `@orange![WARNING]@! Disconnected from Archipelago server. Code: @orange!${event.code}@!`,
      )
    }

    this.socket.onerror = (error) => {
      apError("WebSocket network error:", error)

      // If secure connection fails and we haven't shifted to ws:// yet
      if (!this.isFallbackMode) {
        apWarn(
          `${this.url} connection failed. trying w${this.wss ? "" : "s"}s://${this.hostname}:${this.port}`,
        )

        // Save the preference so next time it skips straight to ws://
        this.wss = !this.wss
        localStorage[this.storageKey] = this.wss
        this.isFallbackMode = true
        this.url = `w${this.wss ? "s" : ""}s://${this.hostname}:${this.port}`

        // Clean up old socket event listeners before retrying
        this.socket.onopen = null
        this.socket.onmessage = null
        this.socket.onclose = null
        this.socket.onerror = null

        this.connect()
      } else {
        localStorage[this.storageKey] = !this.wss
        this.isFallbackMode = false
      }
    }
  }

  /**
   * Standardized helper to transmit packets to the server.
   * @param {Packet[]} packetsArray
   */
  sendPackets(packetsArray) {
    log("SENDING TO SERVER:", JSON.stringify(packetsArray))
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(packetsArray))
    } else {
      apError("Cannot send packet; WebSocket connection is closed.")
    }
  }

  /**
   * Routes inbound packets to their respective protocol handlers based on 'cmd'
   * @param {Packet} packet
   */
  handlePacket(packet) {
    switch (packet.cmd) {
      case "RoomInfo":
        this.onRoomInfo(packet)
        break
      case "Connected":
        this.onConnected(packet)
        break
      case "DataPackage":
        this.onDataPackage(packet)
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
      case "LocationInfo":
        this.onLocationInfo(packet)
        break
      case "Bounced":
        this.onBounced(packet)
        break
      case "Retrieved":
        this.onRetrieved(packet)
        break
      case "SetReply":
        this.onSetReply(packet)
        break
      case "InvalidPacket":
        apError("❌ Archipelago Server rejected payload:", {
          type: packet.type,
          reason: packet.text,
          originalCommand: packet.original_cmd,
        })
        break
      default:
        apLog(`Received unhandled protocol command: ${packet.cmd}`)
    }
  }

  /**
   * @param {Packet} packet
   * @returns {void}
   */
  onRoomUpdate(packet) {
    if (!window.playerLoaded) {
      window.waitingPackets ??= []
      window.waitingPackets.push(packet)
      return
    }
    log(
      "@console!onRoomUpdate@!@blue![Archipelago]@! Room state updated by server.",
    )
    // If other locations were checked (e.g. by a co-op partner in your slot)
    if (packet.checked_locations) {
      this.checkedLocations ??= []

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
        // Also clear it from the in-flight queue: the server has
        // acknowledged this location as checked, whether or not it
        // ends up granting us an item (e.g. it's someone else's item).
        if (window.checksInFlight) {
          const inFlightIdx = window.checksInFlight.indexOf(loc)
          if (inFlightIdx !== -1) {
            window.checksInFlight.splice(inFlightIdx, 1)
          }
        }
      })
    }
    Logic.recompute()
    setTimeout(() => Logic.recompute())
    ItemTracker.render()
  }
  /**
   * Handshake Step 2: Server sends RoomInfo.
   * Handshake Step 5: Client replies with authentication credentials (Connect).
   * @param {Packet} packet
   */
  onRoomInfo(packet) {
    if (window.seed && window.seed != packet.seed_name) {
      warn("page loaded old ap game, reloading!")
      location.reload()
    }
    window.seed = packet.seed_name
    window.history.replaceState(
      {},
      "",
      location.href.replace(/[?&]seed=[^&#]+/, "") +
        "&seed=" +
        packet.seed_name,
    )
    apLog(
      `RoomInfo received. Multiworld Seed: @green!${packet.seed_name}@!`,
    )

    const connectPayload = {
      cmd: "Connect",
      password: this.password,
      game: this.game,
      name: this.playerName,
      uuid: this.generateUUID(),
      version: { major: 0, minor: 6, build: 8, class: "Version" },
      items_handling: 7,
      tags: this.deathLinkEnabled ? ["DeathLink"] : [],
      slot_data: true,
    }

    apLog("Authenticating with server...")

    // Ask the server for the item/location name tables for every game in
    // the room, not just our own — this is what lets us resolve items
    // that come from other players' games.
    this.sendPackets([
      { cmd: "GetDataPackage", games: packet.games },
      connectPayload,
    ])
  }

  /**
   * Server reply to GetDataPackage: per-game item_name_to_id /
   * location_name_to_id tables. We invert them so we can look up a name
   * from an id, keyed by game.
   * @param {Packet} packet
   */
  onDataPackage(packet) {
    for (const [game, gameData] of Object.entries(
      packet.data.games,
    )) {
      this.itemIdToName[game] = {}
      for (const [name, id] of Object.entries(
        gameData.item_name_to_id,
      )) {
        this.itemIdToName[game][id] = name
      }

      this.locationIdToName[game] = {}
      for (const [name, id] of Object.entries(
        gameData.location_name_to_id,
      )) {
        this.locationIdToName[game][id] = name
      }
    }
    apLog(
      `@console!onDataPackage@!@blue![Archipelago]@! Received DataPackage for games: @green!${Object.keys(packet.data.games).join("@!@blue!, @!@green!")}@!`,
    )
  }

  /**
   * Resolve an item id to its display name, given which slot sent it.
   * Falls back to "Unknown Item (id)" if we don't have data for that
   * game yet (e.g. DataPackage hasn't arrived, or slot_info is missing).
   */
  getItemName(itemId, sendingSlot) {
    // log(itemId, this.slotInfo?.[sendingSlot]?.game, format, "itemId, sendingSlot, format")
    const game = this.slotInfo?.[sendingSlot]?.game
    const name = game && this.itemIdToName?.[game]?.[itemId]
    return name ?? `Unknown Item ${game} - (${itemId})`
  }

  /**
   * Handshake Step 6 (Success): Server accepts client authentication.
   */
  onConnected(packet) {
    apLog(
      `@green!Successfully connected!@! Team: @green!${packet.team}@!, Slot ID: @green!${packet.slot}@!`,
    )

    // 1. Mark the client as ready for gameplay packets
    this.isAuthenticated = true
    this.doneConnecting = true
    this.team = packet.team
    this.slot = packet.slot
    this.missingLocations = packet.missing_locations
    this.checkedLocations = packet.checked_locations
    // Maps slot number -> { name, game, type, group_members }
    // This is how we know which game an item with a given sending
    // slot/player number belongs to.
    this.slotInfo = packet.slot_info
    // List of { team, slot, alias, name } - needed to turn "player_id"
    // message parts into readable names.
    this.players = packet.players
    // Per-player options baked in at generation time from their YAML file
    // (via the world's fill_slot_data), e.g. { difficulty: "hard", ... }.
    this.slotData = packet.slot_data ?? {}
    window.onApConnect.forEach((e) => e())

    // Report to the server that this slot is connected and about to
    // begin play (10 = CLIENT_READY).
    this.sendStatusUpdate(10)
  }

  /**
   * Handshake Step 6 (Failure): Server rejects connection credentials.
   * @param {Packet} packet
   */
  onConnectionRefused(packet) {
    this.doneConnecting = true
    apError(
      "Authentication rejected by server. Errors:",
      packet.errors,
    )
  }
  /**
   * Scout locations to see what item they contain, optionally creating a hint.
   * @param {number[]} locationIds - Array of location IDs to scout.
   * @param {number} createAsHint - 0: Don't hint, 1: Hint & broadcast all, 2: Hint & broadcast only new.
   */
  sendLocationScouts(locationIds, createAsHint = 1) {
    if (!this.isAuthenticated) {
      apError(
        "Cannot scout locations yet. Waiting for authentication.",
      )
      return
    }

    const scoutPayload = {
      cmd: "LocationScouts",
      locations: locationIds, // Array of integer location IDs
      create_as_hint: createAsHint, // 1 or 2 will turn this check into a server-tracked hint
    }

    this.sendPackets([scoutPayload])
  }

  /**
   * Server reply to LocationScouts: tells us what item (and whose) actually
   * sits at each scouted location. Resolves both the item name and this
   * player's own location name, caches the result, and notifies any
   * listener (e.g. the map/game code swapping in real icons) via
   * window.onLocationScouted.
   * @param {Packet} packet
   */
  onLocationInfo(packet) {
    const myGame = this.slotInfo?.[this.slot]?.game

    for (const entry of packet.locations || []) {
      const { location, item, player, flags } = entry
      const itemName = this.getItemName(item, player)
      const locationName =
        (myGame && this.locationIdToName?.[myGame]?.[location]) ??
        `Unknown Location (${location})`

      this.scoutedItems[location] = {
        itemName,
        itemPlayer: player,
        locationName,
        flags,
      }
    }
    const pairs = Object.values(ap.locationIdToName.MathQuest).map(
      (str) => {
        var [v, k] = str.split(" - quest:") ?? []
        return [k, v] // Returns [key, value] array
      },
    )

    const result = Object.fromEntries(pairs)
    delete result["undefined"]
    window.questLocations = result
  }

  /**
   * Sends a DeathLink to every other connected client that opted in.
   * Call this when the local player dies, only if deathLinkEnabled.
   * @param {string} cause - human-readable death message, e.g. "Alex fell into lava"
   */
  sendDeathLink(coloredCause) {
    warn(coloredCause, "cause")
    if (!this.deathLinkEnabled) return

    const time = Date.now() / 1000

    this.sendPackets([
      {
        cmd: "Bounce",
        tags: ["DeathLink"],
        data: {
          time,
          cause: removeColors(coloredCause),
          coloredCause,
          source: this.playerName,
        },
      },
    ])
  }

  /**
   * Server reply/relay for Bounce packets. Only cares about ones tagged
   * DeathLink; everything else is ignored (Bounce is a general-purpose
   * relay channel, other tags may be used by other trackers/mods).
   * @param {Packet} packet
   */
  onBounced(packet) {
    warn(packet.tags, "packet.tags")
    if (!packet.tags || !packet.tags.includes("DeathLink")) return
    if (!this.deathLinkEnabled) return

    var { time, cause, source, coloredCause } = packet.data || {}

    // Ignore our own death bouncing back to us.
    // if (source === this.playerName) return
    // Ignore stale duplicates (can happen on reconnect/replay).
    if (this._lastDeathLinkReceivedTime === time) return
    this._lastDeathLinkReceivedTime = time
    if (coloredCause == undefined && cause != undefined) {
      coloredCause = cause
      for (var { name } of Object.values(this.slotInfo)) {
        coloredCause = coloredCause.replace(
          new RegExp(`(?<!\\w)${RegExp.escape(name)}(?!\\w)`),
          `@pink!${name}@!`,
        )
        coloredCause = coloredCause.replace("killed", "@red!killed@!")
      }
    }
    apLog(
      `@red![DeathLink]@! ${coloredCause ? coloredCause : `@pink!${source}@! @red!died@! mysteriously`}`,
    )

    if (source === this.playerName) return
    killPlayer()
  }
  /**
   * Requests a hint from the server using the in-game text command system.
   * @param {string} searchString - The name of the item or location you want a hint for.
   */
  requestItemHint(searchString) {
    if (!this.isAuthenticated) {
      apError("Cannot request hint yet. Waiting for authentication.")
      return
    }

    const sayPayload = {
      cmd: "Say",
      text: `!hint ${searchString}`,
    }

    this.sendPackets([sayPayload])
  }
  /**
   * Handshake Step 7 / Syncing: Server delivers items assigned to this player.
   * @param {Packet} packet
   */
  onReceivedItems(packet) {
    log(`Received packet containing ${packet.items.length} items.`)
    if (!window.playerLoaded) {
      window.waitingPackets ??= []
      window.waitingPackets.push(packet)
      return
    }
    var alreadyReceivedItemsList = []
    packet.items.forEach((item, offset) => {
      this.itemCount += 1
      // item.player is the slot number that SENT this item (the source
      // world), which may be a different game than our own — so we
      // resolve the name via that slot's game, not our own AP_ITEM_IDS.
      const itemName = this.getItemName(item.item, this.slot)
      const senderName = this.players?.find(
        (p) => String(p.slot) === String(item.player),
      )?.alias
      const globalIndex = packet.index + offset
      var itemData = [
        `@${this.itemCount > window.lastReceivedItem ? "purple" : "orange"}![Item Received]@! @console!ID: ${item.item} (@!${formatItemName({ itemName, itemPlayer: this.slot }, true)}${this.itemCount > window.lastReceivedItem ? "" : " - @orange!already recived@!"} - sent by @blue!${senderName}@!@console!`,
        item,
        this.itemCount,
        window.lastReceivedItem,
      ]
      if (this.itemCount <= window.lastReceivedItem) {
        alreadyReceivedItemsList.push(itemData)
        if (alreadyReceivedItemsList.length > 25) {
          alreadyReceivedItemsList.shift()
        }
      } else {
        if (alreadyReceivedItemsList.length) {
          alreadyReceivedItemsList.forEach((e) => apLog(...e))
          alreadyReceivedItemsList = []
        }
        apLog(...itemData)
      }
      if (this.itemCount > window.lastReceivedItem) {
        if (this.itemCount - 1 === window.lastReceivedItem) {
          if (itemList[itemName]) {
            itemList[itemName]()
          } else if (tryGiveLoot(itemName)) {
          } else {
            apError("failed to give", itemName)
          }
          if (manager.mess.__visible) {
            var oldtext = manager.mess.get_text() ?? ""
            manager.mess.set_text(
              `[Item Received] ${itemName}\n${oldtext}`,
            )
          }
        } else {
          apWarn(
            "something went wrong with sending items!!",
            window.lastReceivedItem,
            this.itemCount,
          )
        }
        window.lastReceivedItem = this.itemCount
      }
      this.lastProcessedIndex = globalIndex + 1
    })
    if (alreadyReceivedItemsList.length) {
      alreadyReceivedItemsList.forEach((e) => apLog(...e))
      alreadyReceivedItemsList = []
    }
  }

  /**
   * Turns a single JSONMessagePart into displayable text. This is where
   * raw numeric ids get resolved into real names.
   *
   * Per the AP protocol, `part.player` tells us which slot's *game* the
   * id belongs to (item ids and location ids are only meaningful within
   * a specific game's namespace) — so we look up that slot's game via
   * slot_info, then look up the id in that game's DataPackage tables.
   */
  resolveMessagePart(part) {
    switch (part.type) {
      case "player_id": {
        const player = this.players?.find(
          (p) => String(p.slot) === String(part.text),
        )
        return player ?
            player.alias || player.name
          : `Player ${part.text}`
      }
      case "item_id": {
        const game = this.slotInfo?.[part.player]?.game
        const name = game && this.itemIdToName?.[game]?.[part.text]
        return name ?? `Item #${part.text}`
      }
      case "location_id": {
        const game = this.slotInfo?.[part.player]?.game
        const name =
          game && this.locationIdToName?.[game]?.[part.text]
        return name ?? `Location #${part.text}`
      }
      // "player_name", "item_name", "location_name", "entrance_name",
      // "text", and anything unknown already arrive as plain text.
      default:
        return part.text || ""
    }
  }

  /**
   * Handshake Step 8 / Live Chat: Displays broad multiworld chat notifications.
   */
  onPrintJSON(packet) {
    // Combine text parts into a single string, resolving any id-based
    // parts (player_id / item_id / location_id) to names along the way.
    const messageText = packet.data
      .map((part) => this.resolveMessagePart(part))
      .join("")
    var mt = highlightArray(
      messageText
        .replace(
          /(^[^(]+) \((Team #\d+)\) (playing|tracking|viewing) (.*) has joined/,
          "@green!$1@blue! (@green!$2@blue!) @!$3 @green!$4@! has joined",
        )
        .replace(
          /(^[^(]+) \((Team #\d+)\) has left the game/,
          "@green!$1@blue! (@green!$2@blue!) @! has left the game",
        )
        .replace(
          /(^[^(]+) \((Team #\d+)\) has (started|stopped) (tracking|playing|viewing) the game/,
          "@green!$1@blue! (@!@green!$2@blue!) @! has $3 $4 the game",
        )
        .replace(
          /Client\((\d+)\.(\d+)\.(\d+)\)/,
          "@pink!Client@blue!(@!@green!$1@!@blue!.@!@green!$2@!@blue!.@!@green!$3@!@blue!)@!",
        )
        // 2. Highlight any command starting with ! or / (e.g., !help, /release)
        .replace(/(^|\s)([!/][a-zA-Z_0-9]+)/g, "$1@green!$2@!")

        // 3. Highlight player messages formatted like "Player (Alias): message" or "Player: message"
        // Captures the names/aliases and makes them yellow
        .replace(
          /(^|\]\s)([^:\n]+)\s*\(([^)]+)\):/,
          (_, a, s, d) =>
            `${a}@${d == ap.playerName ? "hotpink" : "yellow"}!${s}(${d})@!:`,
        )
        .replace(
          /(^|\]\s)([^:\n\s]+):(?!\/\/)/,
          (_, a, s) =>
            `${a}@${s == ap.playerName ? "hotpink" : "yellow"}!${s}@!:`,
        )

        // 4. Highlight server options configurations (e.g., "Option hint_cost is set to 10")
        // Colors the option name cyan and the value green
        .replace(
          /(Option\s)([_a-zA-Z0-9]+)(\sis\sset\sto\s)(.*)/g,
          "$1@cyan!$2@!$3@green!$4@!",
        )

        .replace(
          /(Didn't find something that closely matches) '([^']+)' did you mean '([^']+)'\? \((\d+)% sure\)/gm,
          "@red!$1@!",
        )
        .replace(
          new RegExp(
            `'(${Object.keys(itemColors).join("|")}):(\\S+)'`,
            "gm",
          ),
          (_, type, name) =>
            `'@${itemColors[type]}!${type}:${name}@!'`,
        )
        // 5. Highlight common error/denial prefixes (e.g., "Sorry, ...", "Didn't find ...")
        .replace(
          /((?:^|@!) *(?:Sorry|Didn't find|You can't afford)[\w\s\d,]*[.?!]?)/gm,
          "@red!$1@!",
        ),
    )
    for (var { name } of Object.values(this.slotInfo)) {
      mt = mt.replace(
        new RegExp(`(?<!\\w)${RegExp.escape(name)}(?!\\w)`),
        `@pink!${name}@!`,
      )
    }
    mt = mt.replace(
      new RegExp(
        `(?<!\\w)(${Object.keys(itemColors).join("|")}):([\\w.#]+)(?!\\w)`,
        "g",
      ),
      (name) =>
        formatItemName({ itemName: name, itemPlayer: -1 }, true),
    )
    mt = mt.replace(
      /\((\d+)_(\d+) - ([^\)]+)\)/g,
      `@blue!(@!@green!$1_$2@!@blue! - @!$3@blue!)@!`,
    )

    apLog(
      `@console!onPrintJSON@!@blue![Archipelago]@! ${
        mt
        //
      }`,
    )
  }

  /**
   * Application Action: Send items checked inside the game client to the multiworld server.
   * @param {[number]} locationIds
   */
  sendLocationChecks(locationIds) {
    if (!this.isAuthenticated) {
      apError(
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

  /**
   * Application Action: Report this client's ClientStatus to the server.
   * status: 10 = ready, 20 = playing, 30 = goal complete
   * @param {number} status
   */
  sendStatusUpdate(status) {
    if (!this.isAuthenticated) {
      apError(
        "Cannot send status update yet. Waiting for server authentication handshake to complete.",
      )
      return
    }
    if (status === 30 && this.goalCompleteSent) {
      // Already reported goal completion; never send it twice.
      return
    }
    if (status === 30) {
      this.goalCompleteSent = true
    }
    this.sendPackets([{ cmd: "StatusUpdate", status }])
  }

  generateUUID() {
    return Math.random().toString(36).substring(2, 15)
  }

  // Ask for + subscribe to this slot's hint list right after connecting.
  requestHints() {
    const key = `_read_hints_${this.team}_${this.slot}`
    this.sendPackets([
      { cmd: "Get", keys: [key] },
      { cmd: "SetNotify", keys: [key] },
    ])
  }

  // Server replies to Get with "Retrieved"; live changes come as "SetReply".
  onRetrieved(packet) {
    const key = `_read_hints_${this.team}_${this.slot}`
    if (packet.keys?.[key] !== undefined) {
      HintTracker.setHints(packet.keys[key] || [])
    }
  }

  onSetReply(packet) {
    const key = `_read_hints_${this.team}_${this.slot}`
    if (packet.key === key) {
      HintTracker.setHints(packet.value || [])
    }
  }
}
function apTryConnect() {
  window.lastReceivedItem = 0
  if (location.search) {
    var data = location.search
      .replace("?", "")
      .split("&")
      .map((e) => e.split("="))
    var obj = {
      hostname: "127.0.0.1",
      port: "38281",
      game: "MathQuest",
      playerName: "test1",
      password: "",
    }
    for (var [k, v] of data) {
      // Map 'name' from the URL to 'playerName'
      if (k === "name") {
        obj.playerName = decodeURIComponent(v)
      }
      // Split 'connect' into 'hostname' and 'port'
      else if (k === "connect") {
        let parts = v.split(":")
        obj.hostname = parts[0]
        if (parts[1]) {
          obj.port = parts[1]
        }
      }
      // Handle everything else normally
      else {
        obj[k] = decodeURIComponent(v)
      }
    }
    window.ap = new ArchipelagoClient(obj)
    let a = ap.onRoomInfo.bind(ap)
    ap.onRoomInfo = async function (...s) {
      a(...s)
      let data
      if ((data = window.saveData[getSaveFileId()])) {
        var newdata = data["lastReceivedItem"]
        if (isNaN(newdata)) {
          apWarn("newdata was nan")
          newdata = 0
        }
        log(newdata, "newdata")
        window.lastReceivedItem = newdata
        if (window.playerLoaded) {
          for (var packet of window.waitingPackets) {
            ap.handlePacket(packet)
          }
          waitingPackets = []
          // Player is already in-game (20 = CLIENT_PLAYING).
          ap.sendStatusUpdate(20)
        } else {
          window.onPlayerLoaded.push(function () {
            for (var packet of window.waitingPackets) {
              ap.handlePacket(packet)
            }
            waitingPackets = []
            // Player is now actually in-game (20 = CLIENT_PLAYING).
            ap.sendStatusUpdate(20)
          })
        }
      } else {
        createNewSave()
      }
    }
    window.ap.connect()
  }
}
apTryConnect()
window.waitingPackets ??= []
async function get(url) {
  try {
    var resp = await fetch(url)
    if (String(resp.status)[0] == "2") {
      return await resp.json()
    }
    return false
  } catch (e) {
    return false
  }
}
