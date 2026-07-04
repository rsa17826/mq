const itemColors = {
  food: "green",
  item: "brown",
  loot: "brown",
  misc: "purple",
  skill: "yellow",
  craft: "orange",
  trap: "red",
  magic: "purple",
  weapon: "darkgrey",
  armor: "grey",
  permit: "darkorange",
}

/**
 * @typedef {Object} Packet
 * @property {string} cmd
 * @property {any} type
 * @property {string} text
 * @property {string} original_cmd
 * @property {string} seed_name
 * @property {string} games
 * @property {string} errors
 * @property {{games:{location_name_to_id:string}}} data
 */

/**
 * @param {string} name
 * @returns string
 */
function formatItemName(name) {
  var coloredName = name.split(":")
  // @ts-ignore
  coloredName = `@${itemColors[coloredName[0]]}!@console!${coloredName[0]}:@!@${itemColors[coloredName[0]]}!${coloredName[1]}@!`
  return coloredName
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
    this.url = `ws://${hostname}:${port}`
    this.game = game
    this.playerName = playerName
    this.password = password
    this.socket = null
    this.lastProcessedIndex = 0 // Tracks received items to maintain sync
    this.itemCount = 0 // Tracks received items to maintain sync
    this.itemIdToName = {}
    this.locationIdToName = {}
  }

  /**
   * Establishes the WebSocket connection.
   */
  connect() {
    // Note: If running in Node.js, require the 'ws' package: const WebSocket = require('ws');
    this.socket = new WebSocket(this.url)

    this.socket.onopen = () => {
      apLog(
        "WebSocket connection established. Awaiting '@green!RoomInfo@!' from server...",
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
        apError("Failed to parse incoming JSON payload:", err)
      }
    }

    this.socket.onclose = (event) => {
      apWarn(
        `[WARNING] Disconnected from Archipelago server. Code: @orange!${event.code}@!`,
      )
    }

    this.socket.onerror = (error) => {
      apError("WebSocket network error:", error)
    }
  }

  /**
   * Standardized helper to transmit packets to the server.
   */
  sendPackets(packetsArray) {
    log("SENDING TO SERVER:", JSON.stringify(packetsArray)) // <-- Add this line
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
    apLog("@blue![Archipelago]@! Room state updated by server.")
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
      })
    }
  }
  /**
   * Handshake Step 2: Server sends RoomInfo.
   * Handshake Step 5: Client replies with authentication credentials (Connect).
   * @param {Packet} packet
   */
  onRoomInfo(packet) {
    window.seed = packet.seed_name
    apLog(
      `RoomInfo received. Multiworld Seed: @green!${packet.seed_name}@!`,
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
      `@blue![Archipelago]@! Received DataPackage for games: ${Object.keys(packet.data.games).join(", ")}`,
    )
  }

  /**
   * Resolve an item id to its display name, given which slot sent it.
   * Falls back to "Unknown Item (id)" if we don't have data for that
   * game yet (e.g. DataPackage hasn't arrived, or slot_info is missing).
   */
  getItemName(itemId, sendingSlot) {
    const game = this.slotInfo?.[sendingSlot]?.game
    const name = game && this.itemIdToName?.[game]?.[itemId]
    if (game == "MathQuest" && name) {
      return formatItemName(name)
    }
    return name ?? `Unknown Item (${itemId})`
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
  }

  /**
   * Handshake Step 6 (Failure): Server rejects connection credentials.
   * @param {Packet} packet
   */
  onConnectionRefused(packet) {
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

    packet.items.forEach((item, offset) => {
      this.itemCount += 1
      // item.player is the slot number that SENT this item (the source
      // world), which may be a different game than our own — so we
      // resolve the name via that slot's game, not our own AP_ITEM_IDS.
      const itemName =
        this.getItemName(item.item, item.player) ??
        AP_ITEM_IDS[item.item]
      const globalIndex = packet.index + offset

      var coloredName = itemName.split(":")
      coloredName = `@${itemColors[coloredName[0]]}!@console!${coloredName[0]}:@!@${itemColors[coloredName[0]]}!${coloredName[1]}@!`
      apLog(
        `@${this.itemCount > window.lastRecivedItem ? "purple" : "orange"}![Item Received]@! @console!ID: ${item.item} (@!${coloredName}@console!)@!${this.itemCount > window.lastRecivedItem ? "" : " - @orange!already recived@!"}@console!`,
        item,
        this.itemCount,
        window.lastRecivedItem,
      )
      if (this.itemCount > window.lastRecivedItem) {
        if (this.itemCount - 1 === window.lastRecivedItem) {
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
            "somthing went wrong with sending items!!",
            window.lastRecivedItem,
            this.itemCount,
          )
        }
        window.lastRecivedItem = this.itemCount
      }
      this.lastProcessedIndex = globalIndex + 1
    })
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
    apLog(
      `@blue![Archipelago]@! ${
        messageText
          // 1. Original join message formatting
          .replace(
            /(^[^(]+) \((Team #\d+)\) playing (.*) has joined/,
            "@green!$1@blue! (@green!$2@blue!) @!playing @green!$3@! has joined",
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
          )
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

  generateUUID() {
    return Math.random().toString(36).substring(2, 15)
  }
}
window.lastRecivedItem = 0
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
    obj[k] = v
  }
  window.ap = new ArchipelagoClient(obj)
  let a = ap.onRoomInfo.bind(ap)
  ap.onRoomInfo = async function (...s) {
    a(...s)
    let data
    if ((data = await get(`/MQFiles/loadChar_${window.seed}.php`))) {
      var newdata = Number(data.split(" ")[265] ?? "0")
      if (isNaN(newdata)) {
        apWarn("newdata was nan")
        newdata = 0
      }
      log(newdata, "newdata")
      window.lastRecivedItem = newdata
      if (window.playerLoaded) {
        for (var packet of window.waitingPackets) {
          ap.handlePacket(packet)
        }
        waitingPackets = []
      } else {
        window.onPlayerLoaded.push(function () {
          for (var packet of window.waitingPackets) {
            ap.handlePacket(packet)
          }
          waitingPackets = []
        })
      }
    } else {
      get(
        "http://127.0.0.1:1533/cgi-bin/createChar.py?filename=" +
          obj.playerName +
          "&stat0=335&stat1=125&stat2=20&stat3=20&stat4=100&stat5=100&stat6=20&stat7=20&stat8=5&stat9=0&stat10=1&stat11=1&stat12=0&stat13=0&stat14=0&stat15=0&stat16=0&stat17=0&stat18=1&stat19=1&stat20=0&stat21=0&stat22=0&stat23=0&stat24=0&stat25=0&stat26=0&stat27=0&stat28=null&stat29=0&stat30=0&stat31=0&stat32=0&stat33=0&stat34=0&stat35=0&stat36=0&stat37=0&stat38=0&stat39=0&stat40=0&stat41=0&stat42=0&stat43=0&stat44=0&stat45=0&stat46=0&stat47=0&stat48=0&stat49=0&stat50=0&stat51=0&stat52=0&stat53=0&stat54=0&stat55=0&stat56=0&stat57=0&stat58=0&stat59=0&stat60=0&stat61=0&stat62=0&stat63=0&stat64=0&stat65=0&stat66=0&stat67=0&stat68=0&stat69=0&stat70=0&stat71=0&stat72=0&stat73=0&stat74=0&stat75=0&stat76=0&stat77=0&stat78=0&stat79=0&stat80=0&stat81=0&stat82=0&stat83=0&stat84=0&stat85=0&stat86=0&stat87=0&stat88=0&stat89=0&stat90=0&stat91=0&stat92=0&stat93=0&stat94=0&stat95=0&stat96=0&stat97=0&stat98=0&stat99=0&stat100=0&stat101=0&stat102=0&stat103=0&stat104=0&stat105=0&stat106=0&stat107=0&stat108=0&stat109=0&stat110=0&stat111=0&stat112=0&stat113=0&stat114=0&stat115=0&stat116=0&stat117=0&stat118=0&stat119=0&stat120=0&stat121=0&stat122=0&stat123=0&stat124=0&stat125=0&stat126=0&stat127=0&stat128=0&stat129=0&stat130=0&stat131=0&stat132=0&stat133=0&stat134=0&stat135=0&stat136=0&stat137=0&stat138=0&stat139=0&stat140=0&stat141=0&stat142=0&stat143=0&stat144=0&stat145=0&stat146=0&stat147=0&stat148=0&stat149=0&stat150=0&stat151=0&stat152=0&stat153=0&stat154=0&stat155=0&stat156=0&stat157=0&stat158=0&stat159=0&stat160=0&stat161=0&stat162=0&stat163=0&stat164=0&stat165=0&stat166=0&stat167=0&stat168=0&stat169=0&stat170=0&stat171=0&stat172=0&stat173=0&stat174=0&stat175=0&stat176=0&stat177=0&stat178=0&stat179=0&stat180=0&stat181=0&stat182=0&stat183=1&stat184=150&stat185=0&stat186=0&stat187=0&stat188=0&stat189=0&stat190=0&stat191=0&stat192=0&stat193=0&stat194=0&stat195=0&stat196=0&stat197=0&stat198=0&stat199=0&stat200=0&stat201=0&stat202=0&stat203=0&stat204=0&stat205=0&stat206=0&stat207=0&stat208=0&stat209=0&stat210=0&stat211=0&stat212=0&stat213=0&stat214=0&stat215=0&stat216=0&stat217=0&stat218=0&stat219=0&stat220=0&stat221=0&stat222=0&stat223=0&stat224=0&stat225=0&stat226=0&stat227=0&stat228=0&stat229=0&stat230=0&stat231=0&stat232=0&stat233=0&stat234=0&stat235=0&stat236=0&stat237=0&stat238=0&stat239=0&stat240=0&stat241=0&stat242=0&stat243=0&stat244=0&stat245=0&stat246=0&stat247=0&stat248=0&stat249=0&stat250=0&stat251=0&stat252=0&stat253=0&stat254=0&stat255=1&stat256=1&stat257=0&stat258=0&stat259=0&stat260=0&stat261=0&stat262=1&stat263=0&stat264=0&saveFile=" +
          window.seed +
          "&rand=" +
          Math.random(),
      )
    }
  }
  window.ap.connect()
}
window.waitingPackets ??= []
async function get(url) {
  try {
    var resp = await fetch(url)
    if (String(resp.status)[0] == "2") {
      return await resp.text()
    }
    return false
  } catch (e) {
    return false
  }
}
