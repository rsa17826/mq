//a @ts-nocheck
const canvas = document.getElementById("arrow-canvas-2d")
const ctx = canvas.getContext("2d")
const viewport = document.getElementById("viewport")
const grid = document.getElementById("grid")
const panLayer = document.getElementById("pan-layer")
const infoPanel = document.getElementById("info-panel")

let scale = Number(localStorage.scale ?? 0.286)
let originX = 0
let originY = 0
/**
 * @type {string | number | null}
 */
let currentRoom = null
let dashOffset = 0
let isPanning = false
let lastX = 0
let lastY = 0
let needsUpdate = false

/**
 * @type {string | null}
 */
let lastLoadedResolution = null

// =====================================================================
// PATHFINDING
//
// Draws a route from the player's current room to whichever tile (or
// specific entrance on a tile) the mouse is hovering over. Uses
// ap.slotData.roomData when present (handles entrance randomizer),
// otherwise falls back to plain grid-neighbor connections between rooms.
//
// Rooms aren't necessarily "walk in any door, walk out any other door":
// AP_ENTRANCE_IDS[i].areas describes which of a room's exits are freely
// connected to each other, and what's required (permits/items/etc) to
// cross between groups. So the graph here is built at the level of
// individual exits, not whole rooms, and only links two exits within the
// same room if the player could actually currently walk between them.
// =====================================================================

class PathFinding {
  static DIRECT_ARROW_COLOR = "#ff5533"

  static TILE_WIDTH = 710
  static TILE_HEIGHT = 560
  static BLOCKS_X = 14
  static BLOCKS_Y = 11
  static BLOCK_W = PathFinding.TILE_WIDTH / PathFinding.BLOCKS_X
  static BLOCK_H = PathFinding.TILE_HEIGHT / PathFinding.BLOCKS_Y
  // manager.homePoint -> the room it actually teleports you to (kept in sync
  // with whatever sets manager.homePoint in the first place).
  static HOMEPOINT_ROOMS = {
    1: "20_20",
    2: "13_18",
    3: "12_9",
    4: "20_15",
  }

  static OPPOSITE = {
    north: "south",
    south: "north",
    east: "west",
    west: "east",
  }
  // north increases going up (a lower map row), east increases going right.
  static DIR_OFFSET = {
    north: [1, 0],
    south: [-1, 0],
    east: [0, 1],
    west: [0, -1],
  }
  /**
   * @param {any} tok
   */
  static baseTok(tok) {
    return String(tok).split("#")[0]
  }

  /**
   * @param {string} tok
   * @param {{ has: (arg0: any) => any; }} have
   */
  static hasToken(tok, have) {
    if (tok.startsWith("quest:")) {
      return QuestState.satisfied(tok)
    }
    return have.has(tok)
  }

  // reqGroups: array of AND-groups; satisfied if ANY group's tokens are ALL
  // held (OR of ANDs) -- same shape as PROG_DATA's "requires".
  /**
   * @param {any[]} reqGroups
   * @param {any} have
   */
  static reqsSatisfied(reqGroups, have) {
    if (!reqGroups || !reqGroups.length) return true
    return reqGroups.some((/** @type {any[]} */ group) =>
      group.every((/** @type {any} */ tok) =>
        PathFinding.hasToken(PathFinding.baseTok(tok), have),
      ),
    )
  }

  /**
   * @param {string} side
   * @param {number} idx
   */
  static exitKey(side, idx) {
    return `${side}::${idx}`
  }
  /**
   * @param {any} roomKey
   * @param {{ dir: any; idx: any; }} entrance
   */
  static selectionId(roomKey, entrance) {
    return entrance ?
        `${roomKey}::${entrance.dir}::${entrance.idx}`
      : roomKey
  }
  /**
   * @param {any} n
   * @param {any} e
   */
  static roomKey(n, e) {
    return `${n}_${e}`
  }

  // A node is one specific exit of one specific room.
  /**
   * @param {string} roomKey
   * @param {string} side
   * @param {number} idx
   */
  static exitNodeKey(roomKey, side, idx) {
    return `${roomKey}::${side}::${idx}`
  }

  /**
   * @param {{ [x: string]: { fromNode: any; toNode: any; fromRoom: any; fromDir: any; fromIdx: number; toRoom: any; toDir: any; toIdx: number; isWarp: boolean; }[]; }} graph
   * @param {string} fromNode
   * @param {string} toNode
   * @param {string} fromRoom
   * @param {string} fromDir
   * @param {number} fromIdx
   * @param {string} toRoom
   * @param {string} toDir
   * @param {number} toIdx
   * @param {boolean | undefined} [isWarp]
   */
  static addEdge(
    graph,
    fromNode,
    toNode,
    fromRoom,
    fromDir,
    fromIdx,
    toRoom,
    toDir,
    toIdx,
    isWarp,
  ) {
    if (!graph[fromNode]) graph[fromNode] = []
    graph[fromNode].push({
      fromNode,
      toNode,
      fromRoom,
      fromDir,
      fromIdx: Number(fromIdx),
      toRoom,
      toDir,
      toIdx: Number(toIdx),
      isWarp: !!isWarp,
    })
  }
  /**
   * @param {{ AP_ENTRANCE_IDS: any; }} slotData
   */
  static roomsByKey(slotData) {
    const map = {}
    ;(slotData.AP_ENTRANCE_IDS || []).forEach(
      (
        /** @type {{ north: undefined; east: undefined; }} */ room,
      ) => {
        if (
          room &&
          room.north !== undefined &&
          room.east !== undefined
        ) {
          map[PathFinding.roomKey(room.north, room.east)] = room
        }
      },
    )
    return map
  }

  /**
   * @param {{ exits: { [x: string]: any; }; north: number; east: number; }} room
   */
  static roomExitList(room) {
    const list = []
    if (room && room.exits) {
      if (
        (room.north == 10 && room.east == 16) ||
        ((room.north == 6 || room.north == 5) && room.east == 23) ||
        (room.north == 20 && room.east == 12) ||
        (room.north == 18 && room.east == 16)
      ) {
        if (!room.exits?.["north"]?.length)
          list.push({ side: "north", idx: 0 })
        if (!room.exits?.["south"]?.length)
          list.push({ side: "south", idx: 0 })
      }
      Object.keys(room.exits).forEach((side) => {
        const sideList = room.exits[side]
        if (!Array.isArray(sideList)) return
        sideList.forEach((_, idx) => list.push({ side, idx }))
      })
    }
    return list
  }
  // Mirrors regions.py's _connect_warps_vanilla: every connection listed in a
  // warp group -- "root" ones included -- gets a fully bidirectional edge
  // to/from every other connection in that same group. Root is reachable like
  // any other node (fed automatically from its room's real exits, see the
  // root-feed block above) and, once reached, is just as valid a warp origin
  // as a real exit; landing AT root via a warp does NOT grant access to that
  // room's other exits (root has no edge back out to them -- see above), so
  // there's no special expansion here, just a plain edge to the root node.
  //
  // A connection room of (-1, -1) is a wildcard: not a real place, but a
  // stand-in for "wherever the player currently is" (e.g. a "warp" skill
  // castable from anywhere). It's origin-only -- treated as an implicit edge
  // from every real room's root, rather than one fixed node -- since it
  // doesn't correspond to any actual location on the map.
  /**
   * @param {{}} graph
   * @param {{}} roomsByKey
   * @param {Set<string>} have
   */
  static addWarpEdges(graph, roomsByKey, have) {
    const warps =
      (typeof WARPS_DATA !== "undefined" && WARPS_DATA) || []
    warps.forEach(
      (/** @type {{ reqs: any; connections: never[]; }} */ warp) => {
        if (!PathFinding.reqsSatisfied(warp.reqs || [], have)) return
        const conns = warp.connections || []
        conns.forEach(([n, e, side, idx], /** @type {any} */ oi) => {
          const targets = conns.filter(
            (/** @type {any} */ _, /** @type {any} */ di) =>
              di !== oi,
          )
          const isWildcardOrigin = n === -1 && e === -1

          if (isWildcardOrigin) {
            Object.keys(roomsByKey).forEach((roomKey) => {
              const fromNode = PathFinding.exitNodeKey(
                roomKey,
                "root",
                0,
              )
              targets.forEach(([tn, te, tside, tidx]) => {
                const toRoom = `${tn}_${te}`
                const toNode = PathFinding.exitNodeKey(
                  toRoom,
                  tside,
                  tidx,
                )
                PathFinding.addEdge(
                  graph,
                  fromNode,
                  toNode,
                  roomKey,
                  "root",
                  0,
                  toRoom,
                  tside,
                  tidx,
                  true,
                )
              })
            })
            return
          }

          const fromRoom = `${n}_${e}`
          const fromNode = PathFinding.exitNodeKey(
            fromRoom,
            side,
            idx,
          )
          targets.forEach(([tn, te, tside, tidx]) => {
            const toRoom = `${tn}_${te}`
            const toNode = PathFinding.exitNodeKey(
              toRoom,
              tside,
              tidx,
            )
            PathFinding.addEdge(
              graph,
              fromNode,
              toNode,
              fromRoom,
              side,
              idx,
              toRoom,
              tside,
              tidx,
              true,
            )
          })
        })
      },
    )
  }
  // BFS over exit-nodes. The player's current room's own exits all start at
  // distance 0 (we don't track exactly where in the room they're standing,
  // so treat the whole current room as already "at hand").
  /**
   * @param {{ [x: string]: never[]; }} graph
   * @param {{ [x: string]: any; }} roomsByKey
   * @param {string} startRoomKey
   */
  static bfs(graph, roomsByKey, startRoomKey) {
    const dist = {}
    const bestEdge = {}
    const allIncoming = {}
    const queue = []

    // Seed every real exit of the start room AND its root directly: a room
    // that's purely a warp hub (no physical doors at all, just a "root"
    // landing spot) would otherwise never get seeded, since root is normally
    // only fed by an exit->root edge -- and there are no exits here to feed it.
    const rootNode = PathFinding.exitNodeKey(startRoomKey, "root", 0)
    dist[rootNode] = 0
    queue.push(rootNode)
    PathFinding.roomExitList(roomsByKey[startRoomKey]).forEach(
      ({ side, idx }) => {
        const node = PathFinding.exitNodeKey(startRoomKey, side, idx)
        if (dist[node] === undefined) {
          dist[node] = 0
          queue.push(node)
        }
      },
    )

    let qi = 0
    while (qi < queue.length) {
      const cur = queue[qi++]
      const edges = graph[cur] || []
      for (const edge of edges) {
        if (!allIncoming[edge.toNode]) allIncoming[edge.toNode] = []
        allIncoming[edge.toNode].push(edge)
        if (dist[edge.toNode] === undefined) {
          dist[edge.toNode] = dist[cur] + 1
          bestEdge[edge.toNode] = edge
          queue.push(edge.toNode)
        }
      }
    }

    return { dist, bestEdge, allIncoming }
  }

  /**
   * @param {{ [x: string]: any; }} bestEdge
   * @param {string} targetNode
   */
  static reconstructPath(bestEdge, targetNode) {
    const path = []
    let cur = targetNode
    while (bestEdge[cur]) {
      const edge = bestEdge[cur]
      path.unshift(edge)
      cur = edge.fromNode
    }
    return path
  }
  static homePointRoomKey() {
    const hp = window.manager && manager.homePoint
    return PathFinding.HOMEPOINT_ROOMS[hp] || null
  }

  // Every room worth trying as a path's starting point: the player's real
  // current position, always; their current homepoint's room, since
  // teleporting there first might be a shorter overall route; and 20_20
  // specifically whenever they're holding the pendant, since that's an
  // always-available teleport home regardless of the homepoint currently set.
  static candidateStartKeys() {
    const keys = []
    const real = PathFinding.getCurrentRoomKey()
    if (real) keys.push(real)
    const home = PathFinding.homePointRoomKey()
    if (home && !keys.includes(home)) keys.push(home)
    if (
      Logic.haveReal &&
      Logic.haveReal.has("misc:bobbisPendant") &&
      !keys.includes("20_20")
    ) {
      keys.push("20_20")
    }
    return keys
  }
  // --- Pixel geometry, read straight off the rendered tiles ---

  /**
   * @param {any} roomKey
   */
  static tileOrigin(roomKey) {
    const wrapper = document.querySelector(
      `.tile-wrapper[data-room="${roomKey}"]`,
    )
    if (!wrapper) return null
    return {
      x: parseFloat(wrapper.style.left) || 0,
      y: parseFloat(wrapper.style.top) || 0,
    }
  }

  /**
   * @param {string | number} roomKey
   * @param {any} dir
   * @param {string | number} idx
   */
  static findExitData(roomKey, dir, idx) {
    const list =
      (window.EXITS_DATA && window.EXITS_DATA[roomKey]) || []
    const sideMatches = list.filter(
      (/** @type {{ side: any; }} */ e) => e.side === dir,
    )
    return sideMatches[idx] || null
  }

  // Prefer reading the actual rendered .exit-square element (its inline
  // left/top/width/height are percentages of the tile) so the arrow lands
  // exactly on the square the player sees, not just somewhere along that
  // side of the room.
  /**
   * @param {any} roomKey
   * @param {{ x: any; y: any; }} origin
   * @param {any} dir
   * @param {any} idx
   */
  static exitSquareCenter(roomKey, origin, dir, idx) {
    const square = document.querySelector(
      `.exit-square[data-room="${roomKey}"][data-side="${dir}"][data-idx="${idx}"]`,
    )
    if (!square) return null

    const left = parseFloat(square.style.left)
    const top = parseFloat(square.style.top)
    const width = parseFloat(square.style.width)
    const height = parseFloat(square.style.height)
    if ([left, top, width, height].some((n) => Number.isNaN(n)))
      return null

    return {
      x:
        origin.x +
        ((left + width / 2) / 100) * PathFinding.TILE_WIDTH,
      y:
        origin.y +
        ((top + height / 2) / 100) * PathFinding.TILE_HEIGHT,
    }
  }

  // World/grid pixel point for a room's exit in a given direction: the exact
  // center of that exit's square if it's rendered on the page, otherwise the
  // center of its block-range from EXITS_DATA, otherwise the middle of that
  // whole tile edge as a last resort.
  /**
   * @param {any} roomKey
   * @param {string} dir
   * @param {any} idx
   */
  static exitPoint(roomKey, dir, idx) {
    const origin = PathFinding.tileOrigin(roomKey)
    if (!origin) return null

    // Root has no drawn exit-square (it's a landing spot, not a doorway) --
    // resolve it to the room's center instead, same place gen_map.py draws
    // its own root warp markers.
    if (dir === "root") {
      return {
        x: origin.x + PathFinding.TILE_WIDTH / 2,
        y: origin.y + PathFinding.TILE_HEIGHT / 2,
      }
    }

    const squareCenter = PathFinding.exitSquareCenter(
      roomKey,
      origin,
      dir,
      idx,
    )
    if (squareCenter) return squareCenter

    const exit = PathFinding.findExitData(roomKey, dir, idx)

    if (dir === "west" || dir === "east") {
      const top = exit ? exit.top : 0
      const bottom = exit ? exit.bottom : PathFinding.BLOCKS_Y - 1
      const y =
        origin.y + ((top + bottom + 1) / 2) * PathFinding.BLOCK_H
      const x =
        dir === "west" ? origin.x : origin.x + PathFinding.TILE_WIDTH
      return { x, y }
    }

    const left = exit ? exit.left : 0
    const right = exit ? exit.right : PathFinding.BLOCKS_X - 1
    const x =
      origin.x + ((left + right + 1) / 2) * PathFinding.BLOCK_W
    const y =
      dir === "north" ? origin.y : origin.y + PathFinding.TILE_HEIGHT
    return { x, y }
  }

  // Exposed for overlay.js: convert a world-pixel point into a 0..1 fraction
  // of the given room's tile (fx: 0=west edge, 1=east edge; fy: 0=north edge,
  // 1=south edge). Returns null if that room isn't currently rendered.
  /**
   * @param {any} roomKey
   * @param {{ x: number; y: number; }} point
   */
  static worldPointToRoomFraction(roomKey, point) {
    const origin = PathFinding.tileOrigin(roomKey)
    if (!origin) return null
    return {
      fx: (point.x - origin.x) / PathFinding.TILE_WIDTH,
      fy: (point.y - origin.y) / PathFinding.TILE_HEIGHT,
    }
  }
  /**
   * @param {string} roomKey
   */
  static roomCenter(roomKey) {
    const origin = PathFinding.tileOrigin(roomKey)
    if (!origin) return null
    return {
      x: origin.x + PathFinding.TILE_WIDTH / 2,
      y: origin.y + PathFinding.TILE_HEIGHT / 2,
    }
  }

  // A straight dashed "warp" segment representing an instant jump (homepoint
  // teleport, pendant, etc.) from the player's real position to wherever the
  // winning path actually started -- same idea as showDirectArrowTo's pointer,
  // but tagged isWarp so drawArrow renders it dashed like any other warp hop.
  /**
   * @param {string} fromKey
   * @param {any} toKey
   */
  static altStartRoute(fromKey, toKey) {
    const a = PathFinding.roomCenter(fromKey)
    const b = PathFinding.roomCenter(toKey)
    if (!a || !b) return null
    const midX = (a.x + b.x) / 2
    const midY = (a.y + b.y) / 2
    return {
      d: [a.x, a.y, midX, midY, b.x, b.y],
      color: PATH_ARROW_COLOR,
      fromRoom: fromKey,
      fromDir: null,
      fromPoint: a,
      toRoom: toKey,
      toDir: null,
      toPoint: b,
      isWarp: true,
    }
  }

  static getProgData() {
    if (typeof PROG_DATA !== "undefined" && PROG_DATA)
      return PROG_DATA
    if (window.PROG_DATA) return window.PROG_DATA
    return []
  }

  /**
   * @param {string} tok
   */
  static tokenHave(tok) {
    tok = PathFinding.baseTok(tok)
    if (tok.startsWith("quest:")) return QuestState.satisfied(tok)
    return Logic.haveReal.has(tok)
  }

  // Whether one specific (room, token) location has actually been checked --
  // NOT whether the player happens to hold that item type already. The same
  // receive token can be granted by several different physical locations
  // (e.g. several separate "craft:emerald" checks), and holding one copy in
  // haveReal says nothing about which of those specific checks are done.
  // This mirrors logic.js's own per-token "alreadyChecked" test exactly, so
  // tracking and the reachability overlay always agree on what's left.
  /**
   * @param {any} room
   * @param {string} token
   */
  static locationChecked(room, token) {
    token = PathFinding.baseTok(token)
    if (token.startsWith("quest:")) return QuestState.satisfied(token)
    const key = `${room} - ${token}`
    const els = document.querySelectorAll(
      `.progression-icon[data-location="${CSS.escape(key)}"]`,
    )
    return [...els].some((el) => el.classList.contains("checked"))
  } // Some entries live in the virtual/no-location room (e.g. "20_20") and are
  // gated by an area:* requirement instead of having a real physical spot --
  // in that case the place to actually walk to is wherever that area flag is
  // granted, not the virtual room itself. Picks whichever granting location
  // is closest to the player right now (falls back to the first one found).
  /**
   * @param {{ requires: any; }} entry
   */
  static entryAreaToken(entry) {
    for (const group of entry.requires || []) {
      for (const rawTok of group) {
        const tok = PathFinding.baseTok(rawTok)
        if (tok.startsWith("area:")) return tok
      }
    }
    return null
  }

  /**
   * @param {{ room: string; }} entry
   */
  static resolveAreaRedirect(entry) {
    if (!entry || entry.room !== "20_20") return entry
    const areaTok = PathFinding.entryAreaToken(entry)
    if (!areaTok) return entry

    const candidates = PathFinding.getProgData().filter(
      (/** @type {{ room: string; receive: any; }} */ e) =>
        e.room !== "20_20" &&
        (e.receive || []).some(
          (/** @type {any} */ rawTok) =>
            PathFinding.baseTok(rawTok) === areaTok,
        ),
    )
    if (!candidates.length) return entry

    const slotData = window.ap && window.ap.slotData
    const startKey = PathFinding.getCurrentRoomKey()
    if (slotData && startKey) {
      const { graph, roomsByKey } =
        PathFinding.buildPathGraph(slotData)
      if (roomsByKey[startKey]) {
        const { dist } = PathFinding.bfs(graph, roomsByKey, startKey)
        let best = null
        let bestDist = Infinity
        candidates.forEach((/** @type {{ room: any; }} */ c) => {
          const prefix = `${c.room}::`
          for (const node of Object.keys(dist)) {
            if (node.startsWith(prefix) && dist[node] < bestDist) {
              bestDist = dist[node]
              best = c
            }
          }
        })
        if (best) return best
      }
    }
    return candidates[0]
  }

  // --- Loot-progress surfacing ---
  //
  // Requirement groups may include loot:<name>#<count> tokens. When tracking
  // something gated behind loot, surface the still-outstanding loot on the
  // in-game HUD readout (window.extraData), same shape as the game's own
  // loot counters, so the player knows what to go farm first.

  /**
   * @param {string} tok
   */
  static parseLootToken(tok) {
    const m = tok.match(/^loot:([^#]+)#?(\d*)$/)
    if (!m) return null
    return { name: m[1], count: m[2] ? Number(m[2]) : 1 }
  }

  /**
   * @param {{ requires: any; }} entry
   */
  static entryLootTokens(entry) {
    const seen = new Map()
    ;(entry?.requires || []).forEach((/** @type {any[]} */ group) =>
      group.forEach((/** @type {any} */ rawTok) => {
        const parsed = PathFinding.parseLootToken(rawTok)
        if (!parsed) return
        if (
          !seen.has(parsed.name) ||
          seen.get(parsed.name) < parsed.count
        )
          seen.set(parsed.name, parsed.count)
      }),
    )
    return [...seen.entries()]
  }

  // Union-find over one room's exits. Each area-layer whose reqs are
  // satisfied merges together every exit listed in each of its groups.
  // A layer whose reqs aren't satisfied simply contributes no merges this
  // time around -- reqs only ever ADD connections, they never block one
  // that another (satisfied) layer already made. If the room has no `areas`
  // data at all, every exit is merged into one group (fully connected).
  /**
   * @param {{ areas: any[]; }} room
   * @param {Set<string>} have
   */
  static roomConnectivity(room, have) {
    const parent = {}
    /**
     * @param {string} x
     */
    function find(x) {
      if (parent[x] === undefined) parent[x] = x
      if (parent[x] !== x) parent[x] = find(parent[x])
      return parent[x]
    }
    /**
     * @param {string} a
     * @param {string} b
     */
    function union(a, b) {
      const ra = find(a)
      const rb = find(b)
      if (ra !== rb) parent[ra] = rb
    }

    const exits = PathFinding.roomExitList(room)
    exits.forEach(({ side, idx }) =>
      find(PathFinding.exitKey(side, idx)),
    )

    if (
      !room ||
      !Array.isArray(room.areas) ||
      room.areas.length === 0
    ) {
      if (exits.length > 0) {
        const anchor = PathFinding.exitKey(
          exits[0].side,
          exits[0].idx,
        )
        exits.forEach(({ side, idx }) =>
          union(PathFinding.exitKey(side, idx), anchor),
        )
      }
      return { find }
    }

    room.areas.forEach(
      (/** @type {{ reqs: any; areas: any; }} */ layer) => {
        if (!PathFinding.reqsSatisfied(layer.reqs, have)) return
        ;(layer.areas || []).forEach(
          (/** @type {string | any[]} */ group) => {
            for (let i = 1; i < group.length; i++) {
              union(
                PathFinding.exitKey(group[0].side, group[0].idx),
                PathFinding.exitKey(group[i].side, group[i].idx),
              )
            }
          },
        )
      },
    )

    return { find }
  }

  // Re-runs the search and re-points the path arrows (and loot readout).
  // Safe to call anytime; it's a no-op unless something is being tracked.
  static updateTrackedPath() {
    if (!PathFinding.trackedToken) return
    const rawEntry = PathFinding.findTokenEntry(
      PathFinding.trackedToken,
    )
    PathFinding.applyLootTrackingFor(rawEntry)
    if (!rawEntry) {
      PathFinding.clearPathRoute()
      return
    }
    const target = PathFinding.resolveAreaRedirect(rawEntry)
    PathFinding.showPathTo(target.room)
  }

  // Sets (or clears) the HUD loot readout to whatever's still outstanding
  // for `entry`. Safe to call with a null entry to just clear tracking.
  /**
   * @param {{ room: string; requires: never[][] | string[][]; receive: never[] | never[]; }} entry
   */
  static applyLootTrackingFor(entry) {
    const outstanding = PathFinding.entryLootTokens(entry).filter(
      ([name, count]) => {
        const have =
          window.manager?.loot?.[window.Enum?.Loot?.[name]] ?? 0
        return have < count
      },
    )

    if (!outstanding.length) {
      if (PathFinding.lootTrackingList) {
        PathFinding.lootTrackingList = null
        window.extraData = null
      }
      return
    }
    PathFinding.lootTrackingList = outstanding
    window.extraData = PathFinding.buildLootExtraData(outstanding)
  }

  // --- Requirement checking (permits/items gating room-internal crossings) ---

  // Rebuilt on every path request: cheap (a few hundred rooms), and keeps the
  // intra-room edges honest as the player's inventory (`have`) changes.
  /**
   * @param {{ roomData: any[]; }} slotData
   */
  static buildPathGraph(slotData) {
    const graph = {}
    const roomsByKey = PathFinding.roomsByKey(slotData)
    // Prefer the fully-derived set (real items + virtual/free tokens like
    // flags and quests unlocked purely by logic) so a warp/area gated behind
    // a logical flag -- never a real item -- can actually resolve to a
    // walkable path instead of falling back to a "no route" direct arrow.
    // --- Cross-room edges: the physical doorways between rooms ---
    if (
      Array.isArray(slotData.roomData) &&
      slotData.roomData.length
    ) {
      slotData.roomData.forEach(
        (
          /** @type {[any, any, any, any, any, any, any, any]} */ row,
        ) => {
          const [n1, e1, dir1, idx1, n2, e2, dir2, idx2] = row
          const k1 = PathFinding.roomKey(n1, e1)
          const k2 = PathFinding.roomKey(n2, e2)
          const node1 = PathFinding.exitNodeKey(k1, dir1, idx1)
          const node2 = PathFinding.exitNodeKey(k2, dir2, idx2)
          PathFinding.addEdge(
            graph,
            node1,
            node2,
            k1,
            dir1,
            idx1,
            k2,
            dir2,
            idx2,
          )
          PathFinding.addEdge(
            graph,
            node2,
            node1,
            k2,
            dir2,
            idx2,
            k1,
            dir1,
            idx1,
          )
        },
      )
    } else {
      // Fallback (vanilla layout): exit N in a direction connects to exit N
      // (same index) in the opposite direction of the neighboring room.
      Object.keys(roomsByKey).forEach((fromKey) => {
        const room = roomsByKey[fromKey]
        if (!room.exits) return
        Object.keys(room.exits).forEach((dir) => {
          const list = room.exits[dir]
          if (!Array.isArray(list)) return
          const [dn, de] = PathFinding.DIR_OFFSET[dir] || [0, 0]
          const toKey = PathFinding.roomKey(
            room.north + dn,
            room.east + de,
          )
          if (!roomsByKey[toKey]) return
          list.forEach((_, idx) => {
            const oppDir = PathFinding.OPPOSITE[dir]
            const node1 = PathFinding.exitNodeKey(fromKey, dir, idx)
            const node2 = PathFinding.exitNodeKey(toKey, oppDir, idx)
            PathFinding.addEdge(
              graph,
              node1,
              node2,
              fromKey,
              dir,
              idx,
              toKey,
              oppDir,
              idx,
            )
            PathFinding.addEdge(
              graph,
              node2,
              node1,
              toKey,
              oppDir,
              idx,
              fromKey,
              dir,
              idx,
            )
          })
        })
      })
    }

    // --- Intra-room edges: walking between exits inside the same room,
    //     gated by that room's areas/reqs ---
    Object.keys(roomsByKey).forEach((roomKey) => {
      const room = roomsByKey[roomKey]
      const exits = PathFinding.roomExitList(room)
      const conn = PathFinding.roomConnectivity(room, Logic.haveReal)
      for (let i = 0; i < exits.length; i++) {
        for (let j = i + 1; j < exits.length; j++) {
          const a = exits[i]
          const b = exits[j]
          if (
            conn.find(PathFinding.exitKey(a.side, a.idx)) !==
            conn.find(PathFinding.exitKey(b.side, b.idx))
          )
            continue
          const nodeA = PathFinding.exitNodeKey(
            roomKey,
            a.side,
            a.idx,
          )
          const nodeB = PathFinding.exitNodeKey(
            roomKey,
            b.side,
            b.idx,
          )
          PathFinding.addEdge(
            graph,
            nodeA,
            nodeB,
            roomKey,
            a.side,
            a.idx,
            roomKey,
            b.side,
            b.idx,
          )
          PathFinding.addEdge(
            graph,
            nodeB,
            nodeA,
            roomKey,
            b.side,
            b.idx,
            roomKey,
            a.side,
            a.idx,
          )
        }
      }
    })

    // --- Root feed: matches regions.py's Pass 1 exactly -- every real exit
    //     gets a one-way, unconditional edge into its room's single "root"
    //     node, so anything anchored there (a warp) becomes reachable the
    //     moment ANY exit of the room is. Root has no edge back out to real
    //     exits (that's the whole point: the only way out of root is another
    //     warp anchored there), so it's added once per room, not paired. ---
    Object.keys(roomsByKey).forEach((roomKey) => {
      const room = roomsByKey[roomKey]
      const rootNode = PathFinding.exitNodeKey(roomKey, "root", 0)
      PathFinding.roomExitList(room).forEach(({ side, idx }) => {
        const exitNode = PathFinding.exitNodeKey(roomKey, side, idx)
        PathFinding.addEdge(
          graph,
          exitNode,
          rootNode,
          roomKey,
          side,
          idx,
          roomKey,
          "root",
          0,
        )
      })
    })

    // --- Warp edges: teleport-style connections from _room_geometry.WARPS,
    //     gated by their own reqs (same OR-of-AND shape as everything else) ---
    PathFinding.addWarpEdges(graph, roomsByKey, Logic.haveReal)

    return { graph, roomsByKey }
  }
  static getCurrentRoomKey() {
    return PathFinding.roomKey(
      window.player.realnorth,
      window.player.realeast,
    )
  }
  // Path from the player's current room to targetKey. If targetEntrance
  // ({dir, idx}) is given, the route ends specifically through that entrance
  // (may be a hop longer than the shortest room-to-room path). Returns null
  // if there's genuinely no valid route with what the player currently has.
  //
  // Also tries starting from the player's homepoint (and 20_20, if they hold
  // the pendant) as alternate jumping-off points, and picks whichever
  // candidate start actually produces the shortest route. Returns
  // { path, startKey } so callers can tell when the winning route didn't
  // actually start from the player's real position.
  /**
   * @param {any} targetKey
   * @param {{ dir: any; idx: any; }} targetEntrance
   */
  static findPathTo(targetKey, targetEntrance) {
    const slotData = window.ap && window.ap.slotData
    if (!slotData) return null

    const { graph, roomsByKey } = PathFinding.buildPathGraph(slotData)

    const candidates = PathFinding.candidateStartKeys().filter(
      (k) => roomsByKey[k],
    )
    if (!candidates.length) return null

    let best = null // { path, dist, startKey }

    for (const startKey of candidates) {
      if (startKey === targetKey && !targetEntrance)
        return { path: [], startKey } // already there

      const { dist, bestEdge } = PathFinding.bfs(
        graph,
        roomsByKey,
        startKey,
      )

      let path = null
      let pathDist = Infinity

      if (targetEntrance) {
        const targetNode = PathFinding.exitNodeKey(
          targetKey,
          targetEntrance.dir,
          targetEntrance.idx,
        )
        if (dist[targetNode] !== undefined) {
          path = PathFinding.reconstructPath(bestEdge, targetNode)
          pathDist = dist[targetNode]
        }
      } else {
        // No specific entrance requested: take the closest exit-node
        // belonging to that room that's actually reachable.
        const prefix = `${targetKey}::`
        let bestNode = null
        let bestNodeDist = Infinity
        for (const node of Object.keys(dist)) {
          if (node.startsWith(prefix) && dist[node] < bestNodeDist) {
            bestNodeDist = dist[node]
            bestNode = node
          }
        }
        if (bestNode) {
          path = PathFinding.reconstructPath(bestEdge, bestNode)
          pathDist = bestNodeDist
        }
      }

      if (path && pathDist < (best ? best.dist : Infinity)) {
        best = { path, dist: pathDist, startKey }
      }
    }

    return best ? { path: best.path, startKey: best.startKey } : null
  }

  // findPathTo returns null specifically when no valid route exists with
  // what the player currently has/can reach (as opposed to [] for "already
  // there"). In that case, draw a plain straight-line pointer instead of a
  // path, in DIRECT_ARROW_COLOR so it's visually distinct from a real route.
  /**
   * @param {any} targetKey
   */
  static showDirectArrowTo(targetKey) {
    const fromKey = PathFinding.getCurrentRoomKey()
    const a = fromKey && PathFinding.roomCenter(fromKey)
    const b = PathFinding.roomCenter(targetKey)
    if (!a || !b) {
      WorldMap.PATH_ROUTES = []
      WorldMap.requestUpdate()
      return
    }
    const midX = (a.x + b.x) / 2
    const midY = (a.y + b.y) / 2
    WorldMap.PATH_ROUTES = [
      {
        d: [a.x, a.y, midX, midY, b.x, b.y],
        color: PathFinding.DIRECT_ARROW_COLOR,
        fromRoom: fromKey,
        fromDir: null,
        fromPoint: a,
        toRoom: targetKey,
        toDir: null,
        toPoint: b,
      },
    ]
    WorldMap.requestUpdate()
  }

  // Distinct color for "there's genuinely no walkable route right now" so it
  // reads as "go here (somehow)" rather than "walk this exact way".
  // No route found -> falls back to a direct pointer arrow instead of an
  // empty canvas.
  /**
   * @param {any} targetKey
   * @param {undefined} [targetEntrance]
   */
  static showPathTo(targetKey, targetEntrance) {
    const result = PathFinding.findPathTo(targetKey, targetEntrance)
    if (result === null) {
      PathFinding.showDirectArrowTo(targetKey)
      return
    }
    const routes = PathFinding.buildPathRoutes(result.path)
    const realKey = PathFinding.getCurrentRoomKey()
    if (realKey && result.startKey && result.startKey !== realKey) {
      const jump = PathFinding.altStartRoute(realKey, result.startKey)
      if (jump) routes.unshift(jump)
    }
    WorldMap.PATH_ROUTES = routes
    WorldMap.requestUpdate()
  }
  static clearPathRoute() {
    WorldMap.PATH_ROUTES = []
    WorldMap.requestUpdate()
  }

  // =====================================================================
  // TOKEN TRACKING (quests AND items)
  //
  // trackToken("quest:gTree") keeps the path arrows pointed at the next
  // not-yet-completed point of that quest (the lowest "quest:gTree.N" that
  // isn't satisfied yet). trackToken("item:earthAmulet") (or any other exact
  // receive token) points at wherever that token is granted, and stops once
  // the player actually has it. Either way this keeps re-resolving as quest
  // state changes, items come in, or the player moves to a new room.
  //
  // trackQuestPath(questName) is kept as a thin backwards-compatible wrapper
  // around trackToken("quest:" + questName).
  // =====================================================================

  static trackedToken = localStorage.trackedToken || null

  // Scans PROG_DATA for the not-yet-satisfied "quest:<questName>.N" token
  // with the lowest N, and returns the room it's granted in.
  /**
   * @param {any} questName
   */
  static findNextQuestPoint(questName) {
    const prefix = `quest:${questName}.`
    /**
     * @type {{ n: any; room?: any; tok?: string; } | null}
     */
    let best = null

    PathFinding.getProgData().forEach(
      (/** @type {{ receive: any; room: any; }} */ entry) => {
        ;(entry.receive || []).forEach(
          (/** @type {any} */ rawTok) => {
            const tok = PathFinding.baseTok(rawTok)
            if (!tok.startsWith(prefix)) return
            const n = Number(tok.slice(prefix.length))
            if (Number.isNaN(n)) return
            const done = QuestState.satisfied(tok)
            if (done) return
            if (!best || n < best.n)
              best = { room: entry.room, tok, n }
          },
        )
      },
    )

    return best
  }

  // Resolves a tracked token ("quest:<name>" or an exact receive token like
  // "craft:emerald") to the PROG_DATA entry that grants the next
  // not-yet-*checked* instance of it -- checking each (entry.room, token)
  // pairing individually, since several entries (or even one entry with
  // several receive tokens) can share the same token across different
  // physical locations. Returns null once every location granting this token
  // has actually been checked.
  /**
   * @param {string} token
   */
  static findTokenEntry(token) {
    if (!token) return null
    if (token.startsWith("quest:")) {
      const next = PathFinding.findNextQuestPoint(
        token.slice("quest:".length),
      )
      if (!next) return null
      return (
        PathFinding.getProgData().find(
          (/** @type {{ room: any; receive: any; }} */ e) =>
            e.room === next.room &&
            (e.receive || []).some(
              (/** @type {any} */ t) =>
                PathFinding.baseTok(t) === next.tok,
            ),
        ) || { room: next.room, requires: [], receive: [next.tok] }
      )
    }
    for (const entry of PathFinding.getProgData()) {
      if (
        !(entry.receive || []).some(
          (/** @type {any} */ t) => PathFinding.baseTok(t) === token,
        )
      )
        continue
      if (PathFinding.locationChecked(entry.room, token)) continue
      return entry
    }
    return null
  }

  /**
   * @param {string | any[]} path
   */
  static buildPathRoutes(path) {
    if (!path || !path.length) return []
    const routes = []
    for (const edge of path) {
      const a = PathFinding.exitPoint(
        edge.fromRoom,
        edge.fromDir,
        edge.fromIdx,
      )
      const b = PathFinding.exitPoint(
        edge.toRoom,
        edge.toDir,
        edge.toIdx,
      )
      if (!a || !b) continue
      const midX = (a.x + b.x) / 2
      const midY = (a.y + b.y) / 2
      routes.push({
        d: [a.x, a.y, midX, midY, b.x, b.y],
        color: PATH_ARROW_COLOR,
        fromRoom: edge.fromRoom,
        fromDir: edge.fromDir,
        fromPoint: a,
        toRoom: edge.toRoom,
        toDir: edge.toDir,
        toPoint: b,
        isWarp: !!edge.isWarp,
      })
    }
    return routes
  }
  /**
   * @type {[any, any][] | null}
   */
  static lootTrackingList = null

  /**
   * @param {[any, any][]} list
   */
  static buildLootExtraData(list) {
    return () =>
      list
        .map(([name, count]) => {
          const have =
            window.Enum?.Loot?.[name] === undefined ?
              (window.manager?.[name] ?? 0)
            : (window.manager?.loot?.[window.Enum?.Loot?.[name]] ?? 0)
          return have >= count ? "" : `${name}: ${have}/${count}`
        })
        .filter(Boolean)
        .join("\n")
  }
}

const PATH_ARROW_COLOR = "#39ff14"
let selectedPathId = null // identifies whatever room/entrance is currently clicked-on, or null

// Clicking a tile/entrance shows the route to it; clicking the same one
// again clears the route. A manual click always wins over quest tracking.
/**
 * @param {string} roomKey
 * @param {string | undefined} [entrance]
 */
function selectPathTarget(roomKey, entrance) {
  trackedQuestName = null
  const id = PathFinding.selectionId(roomKey, entrance)
  if (selectedPathId === id) {
    selectedPathId = null
    PathFinding.clearPathRoute()
    return
  }
  selectedPathId = id
  localStorage.trackedToken = PathFinding.trackedToken =
    roomKey + " - " + entrance

  PathFinding.showPathTo(roomKey, entrance)
}

class WorldMap {
  static PATH_ROUTES = []
  // Call with an exact token to track: "quest:<name>" chases that quest's
  // next not-yet-satisfied step; any other token (e.g. "item:earthAmulet")
  // chases wherever that exact token is granted. Call with no argument (or a
  // falsy value) to stop tracking.
  /**
   * @param {string | null} token
   */
  static trackToken(token) {
    PathFinding.trackedToken = token || null
    localStorage.trackedToken = PathFinding.trackedToken
    selectedPathId = null // tracking supersedes any manual click-selection
    PathFinding.updateTrackedPath()
  }

  static resizeCanvas() {
    canvas.width = viewport.clientWidth
    canvas.height = viewport.clientHeight
    WorldMap.requestUpdate()
  }

  /**
   * @param {number} x
   * @param {number} y
   */
  static worldToScreen(x, y) {
    return {
      x: x * scale + originX,
      y: y * scale + originY,
    }
  }

  static updateTransform() {
    if (!needsUpdate) return
    panLayer.style.transform = `translate(${originX}px, ${originY}px)`
    grid.style.transform = `scale(${scale})`
    needsUpdate = false
  }

  /**
   * @param {{ d: any; color: any; }} route
   * @param {boolean | undefined} [solid]
   */
  static drawArrow(route, solid) {
    if (!route || !route.d) return

    const nums = route.d
    if (nums.length < 6) return

    let a, b, c
    a = WorldMap.worldToScreen(nums[0], nums[1])
    b = WorldMap.worldToScreen(nums[2], nums[3])
    c = WorldMap.worldToScreen(nums[4], nums[5])

    ctx.beginPath()
    ctx.moveTo(a.x, a.y)
    ctx.quadraticCurveTo(b.x, b.y, c.x, c.y)

    ctx.strokeStyle = route.color
    ctx.lineWidth = solid ? 5 : 4
    ctx.setLineDash(solid ? [] : [12, 8])
    ctx.lineCap = "round"
    ctx.stroke()

    const angle = Math.atan2(c.y - b.y, c.x - b.x)
    const arrowSize = 24

    ctx.beginPath()
    ctx.moveTo(c.x, c.y)
    ctx.lineTo(
      c.x - arrowSize * Math.cos(angle - 0.35),
      c.y - arrowSize * Math.sin(angle - 0.35),
    )
    ctx.lineTo(
      c.x - arrowSize * Math.cos(angle + 0.35),
      c.y - arrowSize * Math.sin(angle + 0.35),
    )
    ctx.closePath()

    ctx.fillStyle = mix(route.color, "#00f2")
    ctx.fill()
  }

  static redrawCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    if (currentRoom) {
      ctx.lineDashOffset = -dashOffset
      dashOffset += 0.4

      const routes = ROUTES_DATA[currentRoom] || []
      routes.forEach((/** @type {any} */ route) =>
        WorldMap.drawArrow(route),
      )
    }

    WorldMap.PATH_ROUTES.forEach(
      (/** @type {{ isWarp: any; }} */ route) =>
        WorldMap.drawArrow(route, !route.isWarp),
    )
  }

  static requestUpdate() {
    if (!needsUpdate) {
      needsUpdate = true
      requestAnimationFrame(() => {
        WorldMap.updateTransform()
        WorldMap.redrawCanvas()
      })
    }
  }
  static updateTileBackgrounds() {
    // Determine target bucket path based on the current viewport layout zoom scale
    let targetResolution = "map_07"
    if (scale >= 3) {
      targetResolution = "map"
    } else if (scale >= 0.55) {
      targetResolution = "map_80"
    } else if (scale >= 0.25) {
      targetResolution = "map_30"
    } else if (scale >= 0.13) {
      targetResolution = "map_20"
    }
    targetResolution = "map_30"

    if (lastLoadedResolution === targetResolution) return
    lastLoadedResolution = targetResolution

    TILES_DATA.forEach(
      (/** @type {{ [x: string]: any; roomKey: any; }} */ tile) => {
        const wrapper = document.querySelector(
          `.tile-wrapper[data-room="${tile.roomKey}"]`,
        )
        if (!wrapper) return

        const imgUrl = tile[targetResolution]

        // Preload smoothly in background cache space to prevent hard screen flashes
        const img = new Image()
        img.src = imgUrl
        img.onload = () => {
          if (lastLoadedResolution === targetResolution) {
            wrapper.style.backgroundImage = `url('${imgUrl}')`
          }
        }
      },
    )
  }
  static init() {
    HookEvent("onQuestChanged", () =>
      setTimeout(PathFinding.updateTrackedPath),
    )
    HookEvent("onQuestChanged", () => Logic.recompute())
    HookEvent("onNewScreen", () => {
      if (
        WorldMap.PATH_ROUTES.find(
          (/** @type {{ toRoom: string; }} */ e) =>
            e.toRoom == `${manager.north}_${manager.east}`,
        )
      ) {
        return
      }
      if (firstLoad) {
        firstLoad = false
        if (/^[\d._]+ - /.test(PathFinding.trackedToken)) {
          var tt = localStorage.trackedToken.split(" - ")
          selectPathTarget(
            tt[0],
            tt[1] !== "undefined" ? tt[1] : undefined,
          )
        } else WorldMap.trackToken(localStorage.trackedToken)
      }
      if (/^[\d._]+ - /.test(PathFinding.trackedToken)) {
        var tt = PathFinding.trackedToken.split(" - ")
        PathFinding.showPathTo(
          tt[0],
          tt[1] !== "undefined" ? tt[1] : undefined,
        )
      } else PathFinding.updateTrackedPath()
    })
    window.addEventListener("resize", WorldMap.resizeCanvas)

    // Smooth memory resolution toggler

    document.addEventListener("DOMContentLoaded", () => {
      toggleCollapse(localStorage.apLogVisible !== "true")
      WorldMap.resizeCanvas()
      WorldMap.updateTileBackgrounds()

      document.querySelectorAll(".tile-wrapper").forEach((tile) => {
        tile.addEventListener("mouseenter", function () {
          currentRoom = this.getAttribute("data-room")
          const rawInfo = this.getAttribute("data-info")
          if (infoPanel && rawInfo) {
            try {
              const infoObj = JSON.parse(rawInfo)
              let htmlContent = `<div class="info-header">Position: ${infoObj.north}, ${infoObj.east}</div>`

              if (infoObj.entries && infoObj.entries.length > 0) {
                infoObj.entries.forEach(
                  (
                    /** @type {{ info: any; requiresHtml: any; receiveHtml: any; }} */ entry,
                    /** @type {number} */ idx,
                  ) => {
                    if (idx > 0) {
                      htmlContent += `<div class="info-event-sep"></div>`
                    }
                    if (infoObj.entries.length > 1) {
                      htmlContent += `<div style="color: #aaa; margin-bottom: 4px;">--- Event #${idx + 1} ---</div>`
                    }
                    if (entry.info) {
                      htmlContent += `<div class="info-line">Info: ${entry.info}</div>`
                    }
                    if (entry.requiresHtml) {
                      htmlContent += `<div class="info-line">Requires: ${entry.requiresHtml}</div>`
                    }
                    if (entry.receiveHtml) {
                      htmlContent += `<div class="info-line">Receive: ${entry.receiveHtml}</div>`
                    }
                  },
                )
              }
              infoPanel.innerHTML = htmlContent
            } catch (e) {
              infoPanel.innerText = rawInfo
            }
          }
          WorldMap.requestUpdate()
        })
        tile.addEventListener("mouseleave", function () {
          currentRoom = null
          if (infoPanel) {
            infoPanel.innerHTML = "Hover over a room to view details."
          }
          WorldMap.requestUpdate()
        })
        tile.addEventListener("click", function (e) {
          selectPathTarget(
            this.getAttribute("data-room").replace("20_16", "19_16"),
          )
        })
      })

      // Clicking a specific entrance/exit square shows the route to that exact
      // entrance instead of just "somewhere in this room". Requires gen_map.py
      // to have been regenerated with data-room/data-side/data-idx attributes
      // on .exit-square elements.
      document
        .querySelectorAll(".exit-square[data-side]")
        .forEach((square) => {
          square.addEventListener("click", function (e) {
            e.stopPropagation()
            const roomKey = this.getAttribute("data-room").replace(
              "20_16",
              "19_16",
            )
            const dir = this.getAttribute("data-side")
            const idx = Number(this.getAttribute("data-idx"))
            selectPathTarget(roomKey, { dir, idx })
          })
        })
    })

    // --- MOUSE PANNING ---
    viewport.addEventListener("mousedown", (e) => {
      if (e.button === 2) {
        isPanning = true
        lastX = e.clientX
        lastY = e.clientY
        viewport.style.cursor = "grabbing"
      }
    })

    window.addEventListener("mousemove", (e) => {
      if (!isPanning) return
      originX += e.clientX - lastX
      originY += e.clientY - lastY
      localStorage.originX = originX
      localStorage.originY = originY
      lastX = e.clientX
      lastY = e.clientY
      WorldMap.requestUpdate()
    })

    window.addEventListener("mouseup", () => {
      isPanning = false
      viewport.style.cursor = "grab"
    })

    // --- MOUSE ZOOM ---
    viewport.addEventListener(
      "wheel",
      (e) => {
        if (
          !isPanning &&
          ItemTracker.itemTrackerPanel?.contains?.(e.target)
        )
          return
        e.preventDefault()
        const zoomIntensity = 0.0009
        const rect = viewport.getBoundingClientRect()
        const mouseX = e.clientX - rect.left
        const mouseY = e.clientY - rect.top

        const prevScale = scale
        scale += -e.deltaY * zoomIntensity
        scale = Math.min(Math.max(0.07, scale), 4)
        localStorage.scale = scale
        originX -= (mouseX - originX) * (scale / prevScale - 1)
        originY -= (mouseY - originY) * (scale / prevScale - 1)
        localStorage.originX = originX
        localStorage.originY = originY
        if (isPanning) {
          lastX = e.clientX
          lastY = e.clientY
        }
        WorldMap.updateTileBackgrounds()
        WorldMap.requestUpdate()
      },
      { passive: false },
    )

    viewport.addEventListener(
      "contextmenu",
      (e) => {
        e.preventDefault()
        e.stopPropagation()
        e.stopImmediatePropagation()
      },
      true,
    )

    function centerMap() {
      originX = Number(
        localStorage.originX ??
          (viewport.clientWidth - grid.offsetWidth * scale) / 2,
      )
      originY = Number(
        localStorage.originY ??
          (viewport.clientHeight - grid.offsetHeight * scale) / 2,
      )
      WorldMap.requestUpdate()
    }

    window.addEventListener("DOMContentLoaded", () => {
      centerMap()
      WorldMap.updateTileBackgrounds()
      viewport.addEventListener(
        "dblclick",
        (e) => {
          if (localStorage.debug != "true") return
          e.preventDefault()
          e.stopPropagation()
          e.stopImmediatePropagation()
          if (
            e.target?.parentElement?.classList?.contains?.(
              "tile-wrapper",
            )
          ) {
            let [an, ae] =
              e.target.parentElement.dataset.room.split("_")
            if (window.player) {
              window.player.realnorth = an
              window.player.realeast = ae
              test.newScreen()
            }
          }
        },
        true,
      )
    })

    setInterval(() => {
      if (currentRoom) {
        WorldMap.redrawCanvas()
      }
    }, 30)
  }
}

var firstLoad = false
window.onPlayerLoaded.push(() => {
  firstLoad = true
})

// Call with a quest key matching ap.slotData.maxQuests / manager.quest[
// Enum.Quest.<name>] (e.g. "gTree") to start tracking it on the map.
// Call with no argument (or a falsy value) to stop tracking.
/**
 * @param {any} questName
 */
function trackQuestPath(questName) {
  trackToken(questName ? `quest:${questName}` : null)
}
window.trackQuestPath = trackQuestPath

// Attaches `handler` to a game hook that might be an array of callbacks,
// an existing function (wrapped so both still run), or not set up yet.
/**
 * @param {string} name
 * @param {function} handler
 */
function HookEvent(name, handler) {
  const existing = window[name]
  if (Array.isArray(existing)) {
    existing.push(handler)
    return
  }
  if (typeof existing === "function") {
    window[name] = function (/** @type {any} */ ...args) {
      existing.apply(this, args)
      handler.apply(this, args)
    }
    return
  }
  window[name] = handler
}
WorldMap.init()
