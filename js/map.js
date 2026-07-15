// @ts-nocheck
const canvas = document.getElementById("arrow-canvas-2d")
const ctx = canvas.getContext("2d")
const viewport = document.getElementById("viewport")
const grid = document.getElementById("grid")
const panLayer = document.getElementById("pan-layer")
const infoPanel = document.getElementById("info-panel")

let scale = Number(localStorage.scale ?? 0.286)
let originX = 0
let originY = 0
let currentRoom = null
let dashOffset = 0
let isPanning = false
let lastX = 0
let lastY = 0
let needsUpdate = false

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

// Must match TILE_WIDTH/TILE_HEIGHT/BLOCKS_X/BLOCKS_Y in gen_map.py
const PF_TILE_WIDTH = 710
const PF_TILE_HEIGHT = 560
const PF_BLOCKS_X = 14
const PF_BLOCKS_Y = 11
const PF_BLOCK_W = PF_TILE_WIDTH / PF_BLOCKS_X
const PF_BLOCK_H = PF_TILE_HEIGHT / PF_BLOCKS_Y

const PF_OPPOSITE = {
  north: "south",
  south: "north",
  east: "west",
  west: "east",
}
// north increases going up (a lower map row), east increases going right.
const PF_DIR_OFFSET = {
  north: [1, 0],
  south: [-1, 0],
  east: [0, 1],
  west: [0, -1],
}

const PATH_ARROW_COLOR = "#39ff14"
window.PATH_ROUTES = []
let selectedPathId = null // identifies whatever room/entrance is currently clicked-on, or null

function pfSelectionId(roomKey, entrance) {
  return entrance ?
      `${roomKey}::${entrance.dir}::${entrance.idx}`
    : roomKey
}

// Clicking a tile/entrance shows the route to it; clicking the same one
// again clears the route. A manual click always wins over quest tracking.
function selectPathTarget(roomKey, entrance) {
  trackedQuestName = null
  const id = pfSelectionId(roomKey, entrance)
  if (selectedPathId === id) {
    selectedPathId = null
    clearPathRoute()
    return
  }
  selectedPathId = id
  localStorage.trackedToken = trackedToken =
    roomKey + " - " + entrance

  showPathTo(roomKey, entrance)
}

function pfRoomKey(n, e) {
  return `${n}_${e}`
}

// A node is one specific exit of one specific room.
function pfExitNodeKey(roomKey, side, idx) {
  return `${roomKey}::${side}::${idx}`
}

function pfAddEdge(
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

// --- Requirement checking (permits/items gating room-internal crossings) ---

function pfBaseTok(tok) {
  return String(tok).split("#")[0]
}

function pfHasToken(tok, have) {
  if (tok.startsWith("quest:")) {
    return QuestState.satisfied(tok)
  }
  return have.has(tok)
}

// reqGroups: array of AND-groups; satisfied if ANY group's tokens are ALL
// held (OR of ANDs) -- same shape as PROG_DATA's "requires".
function pfReqsSatisfied(reqGroups, have) {
  if (!reqGroups || !reqGroups.length) return true
  return reqGroups.some((group) =>
    group.every((tok) => pfHasToken(pfBaseTok(tok), have)),
  )
}

function pfExitKey(side, idx) {
  return `${side}::${idx}`
}

// Union-find over one room's exits. Each area-layer whose reqs are
// satisfied merges together every exit listed in each of its groups.
// A layer whose reqs aren't satisfied simply contributes no merges this
// time around -- reqs only ever ADD connections, they never block one
// that another (satisfied) layer already made. If the room has no `areas`
// data at all, every exit is merged into one group (fully connected).
function pfRoomConnectivity(room, have) {
  const parent = {}
  function find(x) {
    if (parent[x] === undefined) parent[x] = x
    if (parent[x] !== x) parent[x] = find(parent[x])
    return parent[x]
  }
  function union(a, b) {
    const ra = find(a)
    const rb = find(b)
    if (ra !== rb) parent[ra] = rb
  }

  const exits = pfRoomExitList(room)
  exits.forEach(({ side, idx }) => find(pfExitKey(side, idx)))

  if (
    !room ||
    !Array.isArray(room.areas) ||
    room.areas.length === 0
  ) {
    if (exits.length > 0) {
      const anchor = pfExitKey(exits[0].side, exits[0].idx)
      exits.forEach(({ side, idx }) =>
        union(pfExitKey(side, idx), anchor),
      )
    }
    return { find }
  }

  room.areas.forEach((layer) => {
    if (!pfReqsSatisfied(layer.reqs, have)) return
    ;(layer.areas || []).forEach((group) => {
      for (let i = 1; i < group.length; i++) {
        union(
          pfExitKey(group[0].side, group[0].idx),
          pfExitKey(group[i].side, group[i].idx),
        )
      }
    })
  })

  return { find }
}

function pfRoomsByKey(slotData) {
  const map = {}
  ;(slotData.AP_ENTRANCE_IDS || []).forEach((room) => {
    if (room && room.north !== undefined && room.east !== undefined) {
      map[pfRoomKey(room.north, room.east)] = room
    }
  })
  return map
}

function pfRoomExitList(room) {
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

// Rebuilt on every path request: cheap (a few hundred rooms), and keeps the
// intra-room edges honest as the player's inventory (`have`) changes.
function buildPathGraph(slotData) {
  const graph = {}
  const roomsByKey = pfRoomsByKey(slotData)
  // Prefer the fully-derived set (real items + virtual/free tokens like
  // flags and quests unlocked purely by logic) so a warp/area gated behind
  // a logical flag -- never a real item -- can actually resolve to a
  // walkable path instead of falling back to a "no route" direct arrow.
  const have = window.haveDerived || window.haveReal || new Set()

  // --- Cross-room edges: the physical doorways between rooms ---
  if (Array.isArray(slotData.roomData) && slotData.roomData.length) {
    slotData.roomData.forEach((row) => {
      const [n1, e1, dir1, idx1, n2, e2, dir2, idx2] = row
      const k1 = pfRoomKey(n1, e1)
      const k2 = pfRoomKey(n2, e2)
      const node1 = pfExitNodeKey(k1, dir1, idx1)
      const node2 = pfExitNodeKey(k2, dir2, idx2)
      pfAddEdge(graph, node1, node2, k1, dir1, idx1, k2, dir2, idx2)
      pfAddEdge(graph, node2, node1, k2, dir2, idx2, k1, dir1, idx1)
    })
  } else {
    // Fallback (vanilla layout): exit N in a direction connects to exit N
    // (same index) in the opposite direction of the neighboring room.
    Object.keys(roomsByKey).forEach((fromKey) => {
      const room = roomsByKey[fromKey]
      if (!room.exits) return
      Object.keys(room.exits).forEach((dir) => {
        const list = room.exits[dir]
        if (!Array.isArray(list)) return
        const [dn, de] = PF_DIR_OFFSET[dir] || [0, 0]
        const toKey = pfRoomKey(room.north + dn, room.east + de)
        if (!roomsByKey[toKey]) return
        list.forEach((_, idx) => {
          const oppDir = PF_OPPOSITE[dir]
          const node1 = pfExitNodeKey(fromKey, dir, idx)
          const node2 = pfExitNodeKey(toKey, oppDir, idx)
          pfAddEdge(
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
          pfAddEdge(
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
    const exits = pfRoomExitList(room)
    const conn = pfRoomConnectivity(room, have)
    for (let i = 0; i < exits.length; i++) {
      for (let j = i + 1; j < exits.length; j++) {
        const a = exits[i]
        const b = exits[j]
        if (
          conn.find(pfExitKey(a.side, a.idx)) !==
          conn.find(pfExitKey(b.side, b.idx))
        )
          continue
        const nodeA = pfExitNodeKey(roomKey, a.side, a.idx)
        const nodeB = pfExitNodeKey(roomKey, b.side, b.idx)
        pfAddEdge(
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
        pfAddEdge(
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
    const rootNode = pfExitNodeKey(roomKey, "root", 0)
    pfRoomExitList(room).forEach(({ side, idx }) => {
      const exitNode = pfExitNodeKey(roomKey, side, idx)
      pfAddEdge(
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
  pfAddWarpEdges(graph, roomsByKey, have)

  return { graph, roomsByKey }
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
function pfAddWarpEdges(graph, roomsByKey, have) {
  const warps =
    (typeof WARPS_DATA !== "undefined" && WARPS_DATA) || []
  warps.forEach((warp) => {
    if (!pfReqsSatisfied(warp.reqs || [], have)) return
    const conns = warp.connections || []
    conns.forEach(([n, e, side, idx], oi) => {
      const targets = conns.filter((_, di) => di !== oi)
      const isWildcardOrigin = n === -1 && e === -1

      if (isWildcardOrigin) {
        Object.keys(roomsByKey).forEach((roomKey) => {
          const fromNode = pfExitNodeKey(roomKey, "root", 0)
          targets.forEach(([tn, te, tside, tidx]) => {
            const toRoom = `${tn}_${te}`
            const toNode = pfExitNodeKey(toRoom, tside, tidx)
            pfAddEdge(
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
      const fromNode = pfExitNodeKey(fromRoom, side, idx)
      targets.forEach(([tn, te, tside, tidx]) => {
        const toRoom = `${tn}_${te}`
        const toNode = pfExitNodeKey(toRoom, tside, tidx)
        pfAddEdge(
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
  })
}

// Adjust here if the game exposes the player's current room differently.
function getCurrentRoomKey() {
  if (
    window.player &&
    window.player.realnorth !== undefined &&
    window.player.realeast !== undefined
  ) {
    return pfRoomKey(window.player.realnorth, window.player.realeast)
  }
  if (
    window.player &&
    window.player.north !== undefined &&
    window.player.east !== undefined
  ) {
    return pfRoomKey(window.player.north, window.player.east)
  }
  return null
}

// BFS over exit-nodes. The player's current room's own exits all start at
// distance 0 (we don't track exactly where in the room they're standing,
// so treat the whole current room as already "at hand").
function pfBfs(graph, roomsByKey, startRoomKey) {
  const dist = {}
  const bestEdge = {}
  const allIncoming = {}
  const queue = []

  // Seed every real exit of the start room AND its root directly: a room
  // that's purely a warp hub (no physical doors at all, just a "root"
  // landing spot) would otherwise never get seeded, since root is normally
  // only fed by an exit->root edge -- and there are no exits here to feed it.
  const rootNode = pfExitNodeKey(startRoomKey, "root", 0)
  dist[rootNode] = 0
  queue.push(rootNode)
  pfRoomExitList(roomsByKey[startRoomKey]).forEach(
    ({ side, idx }) => {
      const node = pfExitNodeKey(startRoomKey, side, idx)
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

function pfReconstructPath(bestEdge, targetNode) {
  const path = []
  let cur = targetNode
  while (bestEdge[cur]) {
    const edge = bestEdge[cur]
    path.unshift(edge)
    cur = edge.fromNode
  }
  return path
}

// manager.homePoint -> the room it actually teleports you to (kept in sync
// with whatever sets manager.homePoint in the first place).
const HOMEPOINT_ROOMS = {
  1: "20_20",
  2: "13_18",
  3: "12_9",
  4: "20_15",
}

function pfHomePointRoomKey() {
  const hp = window.manager && manager.homePoint
  return HOMEPOINT_ROOMS[hp] || null
}

// Every room worth trying as a path's starting point: the player's real
// current position, always; their current homepoint's room, since
// teleporting there first might be a shorter overall route; and 20_20
// specifically whenever they're holding the pendant, since that's an
// always-available teleport home regardless of the homepoint currently set.
function pfCandidateStartKeys() {
  const keys = []
  const real = getCurrentRoomKey()
  if (real) keys.push(real)
  const home = pfHomePointRoomKey()
  if (home && !keys.includes(home)) keys.push(home)
  const have = window.haveDerived || window.haveReal
  if (
    have &&
    have.has("misc:bobbisPendant") &&
    !keys.includes("20_20")
  ) {
    keys.push("20_20")
  }
  return keys
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
function findPathTo(targetKey, targetEntrance) {
  const slotData = window.ap && window.ap.slotData
  if (!slotData) return null

  const { graph, roomsByKey } = buildPathGraph(slotData)

  const candidates = pfCandidateStartKeys().filter(
    (k) => roomsByKey[k],
  )
  if (!candidates.length) return null

  let best = null // { path, dist, startKey }

  for (const startKey of candidates) {
    if (startKey === targetKey && !targetEntrance)
      return { path: [], startKey } // already there

    const { dist, bestEdge } = pfBfs(graph, roomsByKey, startKey)

    let path = null
    let pathDist = Infinity

    if (targetEntrance) {
      const targetNode = pfExitNodeKey(
        targetKey,
        targetEntrance.dir,
        targetEntrance.idx,
      )
      if (dist[targetNode] !== undefined) {
        path = pfReconstructPath(bestEdge, targetNode)
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
        path = pfReconstructPath(bestEdge, bestNode)
        pathDist = bestNodeDist
      }
    }

    if (path && pathDist < (best ? best.dist : Infinity)) {
      best = { path, dist: pathDist, startKey }
    }
  }

  return best ? { path: best.path, startKey: best.startKey } : null
}

// --- Pixel geometry, read straight off the rendered tiles ---

function pfTileOrigin(roomKey) {
  const wrapper = document.querySelector(
    `.tile-wrapper[data-room="${roomKey}"]`,
  )
  if (!wrapper) return null
  return {
    x: parseFloat(wrapper.style.left) || 0,
    y: parseFloat(wrapper.style.top) || 0,
  }
}

function pfFindExitData(roomKey, dir, idx) {
  const list = (window.EXITS_DATA && window.EXITS_DATA[roomKey]) || []
  const sideMatches = list.filter((e) => e.side === dir)
  return sideMatches[idx] || null
}

// Prefer reading the actual rendered .exit-square element (its inline
// left/top/width/height are percentages of the tile) so the arrow lands
// exactly on the square the player sees, not just somewhere along that
// side of the room.
function pfExitSquareCenter(roomKey, origin, dir, idx) {
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
    x: origin.x + ((left + width / 2) / 100) * PF_TILE_WIDTH,
    y: origin.y + ((top + height / 2) / 100) * PF_TILE_HEIGHT,
  }
}

// World/grid pixel point for a room's exit in a given direction: the exact
// center of that exit's square if it's rendered on the page, otherwise the
// center of its block-range from EXITS_DATA, otherwise the middle of that
// whole tile edge as a last resort.
function pfExitPoint(roomKey, dir, idx) {
  const origin = pfTileOrigin(roomKey)
  if (!origin) return null

  // Root has no drawn exit-square (it's a landing spot, not a doorway) --
  // resolve it to the room's center instead, same place gen_map.py draws
  // its own root warp markers.
  if (dir === "root") {
    return {
      x: origin.x + PF_TILE_WIDTH / 2,
      y: origin.y + PF_TILE_HEIGHT / 2,
    }
  }

  const squareCenter = pfExitSquareCenter(roomKey, origin, dir, idx)
  if (squareCenter) return squareCenter

  const exit = pfFindExitData(roomKey, dir, idx)

  if (dir === "west" || dir === "east") {
    const top = exit ? exit.top : 0
    const bottom = exit ? exit.bottom : PF_BLOCKS_Y - 1
    const y = origin.y + ((top + bottom + 1) / 2) * PF_BLOCK_H
    const x = dir === "west" ? origin.x : origin.x + PF_TILE_WIDTH
    return { x, y }
  }

  const left = exit ? exit.left : 0
  const right = exit ? exit.right : PF_BLOCKS_X - 1
  const x = origin.x + ((left + right + 1) / 2) * PF_BLOCK_W
  const y = dir === "north" ? origin.y : origin.y + PF_TILE_HEIGHT
  return { x, y }
}

// Exposed for overlay.js: convert a world-pixel point into a 0..1 fraction
// of the given room's tile (fx: 0=west edge, 1=east edge; fy: 0=north edge,
// 1=south edge). Returns null if that room isn't currently rendered.
function pfWorldPointToRoomFraction(roomKey, point) {
  const origin = pfTileOrigin(roomKey)
  if (!origin) return null
  return {
    fx: (point.x - origin.x) / PF_TILE_WIDTH,
    fy: (point.y - origin.y) / PF_TILE_HEIGHT,
  }
}
window.pfWorldPointToRoomFraction = pfWorldPointToRoomFraction

function buildPathRoutes(path) {
  if (!path || !path.length) return []
  const routes = []
  for (const edge of path) {
    const a = pfExitPoint(edge.fromRoom, edge.fromDir, edge.fromIdx)
    const b = pfExitPoint(edge.toRoom, edge.toDir, edge.toIdx)
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

// Distinct color for "there's genuinely no walkable route right now" so it
// reads as "go here (somehow)" rather than "walk this exact way".
const DIRECT_ARROW_COLOR = "#ff5533"

function pfRoomCenter(roomKey) {
  const origin = pfTileOrigin(roomKey)
  if (!origin) return null
  return {
    x: origin.x + PF_TILE_WIDTH / 2,
    y: origin.y + PF_TILE_HEIGHT / 2,
  }
}

// findPathTo returns null specifically when no valid route exists with
// what the player currently has/can reach (as opposed to [] for "already
// there"). In that case, draw a plain straight-line pointer instead of a
// path, in DIRECT_ARROW_COLOR so it's visually distinct from a real route.
function showDirectArrowTo(targetKey) {
  const fromKey = getCurrentRoomKey()
  const a = fromKey && pfRoomCenter(fromKey)
  const b = pfRoomCenter(targetKey)
  if (!a || !b) {
    window.PATH_ROUTES = []
    requestUpdate()
    return
  }
  const midX = (a.x + b.x) / 2
  const midY = (a.y + b.y) / 2
  window.PATH_ROUTES = [
    {
      d: [a.x, a.y, midX, midY, b.x, b.y],
      color: DIRECT_ARROW_COLOR,
      fromRoom: fromKey,
      fromDir: null,
      fromPoint: a,
      toRoom: targetKey,
      toDir: null,
      toPoint: b,
    },
  ]
  requestUpdate()
}

// A straight dashed "warp" segment representing an instant jump (homepoint
// teleport, pendant, etc.) from the player's real position to wherever the
// winning path actually started -- same idea as showDirectArrowTo's pointer,
// but tagged isWarp so drawArrow renders it dashed like any other warp hop.
function pfAltStartRoute(fromKey, toKey) {
  const a = pfRoomCenter(fromKey)
  const b = pfRoomCenter(toKey)
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

// No route found -> falls back to a direct pointer arrow instead of an
// empty canvas.
function showPathTo(targetKey, targetEntrance) {
  const result = findPathTo(targetKey, targetEntrance)
  if (result === null) {
    showDirectArrowTo(targetKey)
    return
  }
  const routes = buildPathRoutes(result.path)
  const realKey = getCurrentRoomKey()
  if (realKey && result.startKey && result.startKey !== realKey) {
    const jump = pfAltStartRoute(realKey, result.startKey)
    if (jump) routes.unshift(jump)
  }
  window.PATH_ROUTES = routes
  requestUpdate()
}

function clearPathRoute() {
  window.PATH_ROUTES = []
  requestUpdate()
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

let trackedToken = localStorage.trackedToken || null

function pfGetProgData() {
  if (typeof PROG_DATA !== "undefined" && PROG_DATA) return PROG_DATA
  if (window.PROG_DATA) return window.PROG_DATA
  return []
}

function pfTokenHave(tok) {
  tok = pfBaseTok(tok)
  if (tok.startsWith("quest:")) return QuestState.satisfied(tok)
  return (window.haveDerived || window.haveReal || new Set()).has(tok)
}

// Whether one specific (room, token) location has actually been checked --
// NOT whether the player happens to hold that item type already. The same
// receive token can be granted by several different physical locations
// (e.g. several separate "craft:emerald" checks), and holding one copy in
// haveReal says nothing about which of those specific checks are done.
// This mirrors logic.js's own per-token "alreadyChecked" test exactly, so
// tracking and the reachability overlay always agree on what's left.
function pfLocationChecked(room, token) {
  token = pfBaseTok(token)
  if (token.startsWith("quest:")) return QuestState.satisfied(token)
  const key = `${room} - ${token}`
  const els = document.querySelectorAll(
    `.progression-icon[data-location="${CSS.escape(key)}"]`,
  )
  return [...els].some((el) => el.classList.contains("checked"))
}
window.pfLocationChecked = pfLocationChecked

// Scans PROG_DATA for the not-yet-satisfied "quest:<questName>.N" token
// with the lowest N, and returns the room it's granted in.
function findNextQuestPoint(questName) {
  const prefix = `quest:${questName}.`
  let best = null

  pfGetProgData().forEach((entry) => {
    ;(entry.receive || []).forEach((rawTok) => {
      const tok = pfBaseTok(rawTok)
      if (!tok.startsWith(prefix)) return
      const n = Number(tok.slice(prefix.length))
      if (Number.isNaN(n)) return
      const done = QuestState.satisfied(tok)
      if (done) return
      if (!best || n < best.n) best = { room: entry.room, tok, n }
    })
  })

  return best
}

// Resolves a tracked token ("quest:<name>" or an exact receive token like
// "craft:emerald") to the PROG_DATA entry that grants the next
// not-yet-*checked* instance of it -- checking each (entry.room, token)
// pairing individually, since several entries (or even one entry with
// several receive tokens) can share the same token across different
// physical locations. Returns null once every location granting this token
// has actually been checked.
function findTokenEntry(token) {
  if (!token) return null
  if (token.startsWith("quest:")) {
    const next = findNextQuestPoint(token.slice("quest:".length))
    if (!next) return null
    return (
      pfGetProgData().find(
        (e) =>
          e.room === next.room &&
          (e.receive || []).some((t) => pfBaseTok(t) === next.tok),
      ) || { room: next.room, requires: [], receive: [next.tok] }
    )
  }
  for (const entry of pfGetProgData()) {
    if (!(entry.receive || []).some((t) => pfBaseTok(t) === token))
      continue
    if (pfLocationChecked(entry.room, token)) continue
    return entry
  }
  return null
}

// Some entries live in the virtual/no-location room (e.g. "20_20") and are
// gated by an area:* requirement instead of having a real physical spot --
// in that case the place to actually walk to is wherever that area flag is
// granted, not the virtual room itself. Picks whichever granting location
// is closest to the player right now (falls back to the first one found).
function pfEntryAreaToken(entry) {
  for (const group of entry.requires || []) {
    for (const rawTok of group) {
      const tok = pfBaseTok(rawTok)
      if (tok.startsWith("area:")) return tok
    }
  }
  return null
}

function pfResolveAreaRedirect(entry) {
  if (!entry || entry.room !== "20_20") return entry
  const areaTok = pfEntryAreaToken(entry)
  if (!areaTok) return entry

  const candidates = pfGetProgData().filter(
    (e) =>
      e.room !== "20_20" &&
      (e.receive || []).some(
        (rawTok) => pfBaseTok(rawTok) === areaTok,
      ),
  )
  if (!candidates.length) return entry

  const slotData = window.ap && window.ap.slotData
  const startKey = getCurrentRoomKey()
  if (slotData && startKey) {
    const { graph, roomsByKey } = buildPathGraph(slotData)
    if (roomsByKey[startKey]) {
      const { dist } = pfBfs(graph, roomsByKey, startKey)
      let best = null
      let bestDist = Infinity
      candidates.forEach((c) => {
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

function pfParseLootToken(tok) {
  const m = tok.match(/^loot:([^#]+)#?(\d*)$/)
  if (!m) return null
  return { name: m[1], count: m[2] ? Number(m[2]) : 1 }
}

function pfEntryLootTokens(entry) {
  const seen = new Map()
  ;(entry?.requires || []).forEach((group) =>
    group.forEach((rawTok) => {
      const parsed = pfParseLootToken(rawTok)
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

const __origExtraData = window.extraData
let lootTrackingList = null

function buildLootExtraData(list) {
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

// Sets (or clears) the HUD loot readout to whatever's still outstanding
// for `entry`. Safe to call with a null entry to just clear tracking.
function applyLootTrackingFor(entry) {
  const outstanding = pfEntryLootTokens(entry).filter(
    ([name, count]) => {
      const have =
        window.manager?.loot?.[window.Enum?.Loot?.[name]] ?? 0
      return have < count
    },
  )

  if (!outstanding.length) {
    if (lootTrackingList) {
      lootTrackingList = null
      window.extraData = __origExtraData
    }
    return
  }
  lootTrackingList = outstanding
  window.extraData = buildLootExtraData(outstanding)
}
window.applyLootTrackingFor = applyLootTrackingFor

// Re-runs the search and re-points the path arrows (and loot readout).
// Safe to call anytime; it's a no-op unless something is being tracked.
function updateTrackedPath() {
  if (!trackedToken) return
  const rawEntry = findTokenEntry(trackedToken)
  applyLootTrackingFor(rawEntry)
  if (!rawEntry) {
    clearPathRoute()
    return
  }
  const target = pfResolveAreaRedirect(rawEntry)
  showPathTo(target.room)
}

// Call with an exact token to track: "quest:<name>" chases that quest's
// next not-yet-satisfied step; any other token (e.g. "item:earthAmulet")
// chases wherever that exact token is granted. Call with no argument (or a
// falsy value) to stop tracking.
function trackToken(token) {
  trackedToken = token || null
  localStorage.trackedToken = trackedToken
  selectedPathId = null // tracking supersedes any manual click-selection
  updateTrackedPath()
}
window.trackToken = trackToken
var firstLoad = false
window.onPlayerLoaded.push(() => {
  firstLoad = true
})

// Call with a quest key matching ap.slotData.maxQuests / manager.quest[
// Enum.Quest.<name>] (e.g. "gTree") to start tracking it on the map.
// Call with no argument (or a falsy value) to stop tracking.
function trackQuestPath(questName) {
  trackToken(questName ? `quest:${questName}` : null)
}
window.trackQuestPath = trackQuestPath

// Attaches `handler` to a game hook that might be an array of callbacks,
// an existing function (wrapped so both still run), or not set up yet.
function pfHookEvent(name, handler) {
  const existing = window[name]
  if (Array.isArray(existing)) {
    existing.push(handler)
    return
  }
  if (typeof existing === "function") {
    window[name] = function (...args) {
      existing.apply(this, args)
      handler.apply(this, args)
    }
    return
  }
  window[name] = handler
}

pfHookEvent("onQuestChanged", () => setTimeout(updateTrackedPath))
pfHookEvent("onQuestChanged", () => window.__trackerRecompute?.())
pfHookEvent("onNewScreen", () => {
  if (
    window.PATH_ROUTES.find(
      (e) => e.toRoom == `${manager.north}_${manager.east}`,
    )
  ) {
    return
  }
  if (firstLoad) {
    firstLoad = false
    if (/^[\d._]+ - /.test(trackedToken)) {
      var tt = localStorage.trackedToken.split(" - ")
      selectPathTarget(
        tt[0],
        tt[1] !== "undefined" ? tt[1] : undefined,
      )
    } else trackToken(localStorage.trackedToken)
  }
  if (/^[\d._]+ - /.test(trackedToken)) {
    var tt = trackedToken.split(" - ")
    showPathTo(tt[0], tt[1] !== "undefined" ? tt[1] : undefined)
  } else updateTrackedPath()
})

function resizeCanvas() {
  canvas.width = viewport.clientWidth
  canvas.height = viewport.clientHeight
  requestUpdate()
}
window.addEventListener("resize", resizeCanvas)

// Smooth memory resolution toggler
function updateTileBackgrounds() {
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

  TILES_DATA.forEach((tile) => {
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
  })
}

document.addEventListener("DOMContentLoaded", () => {
  toggleCollapse(localStorage.apLogVisible !== "true")
  resizeCanvas()
  updateTileBackgrounds()

  document.querySelectorAll(".tile-wrapper").forEach((tile) => {
    tile.addEventListener("mouseenter", function () {
      currentRoom = this.getAttribute("data-room")
      const rawInfo = this.getAttribute("data-info")
      if (infoPanel && rawInfo) {
        try {
          const infoObj = JSON.parse(rawInfo)
          let htmlContent = `<div class="info-header">Position: ${infoObj.north}, ${infoObj.east}</div>`

          if (infoObj.entries && infoObj.entries.length > 0) {
            infoObj.entries.forEach((entry, idx) => {
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
            })
          }
          infoPanel.innerHTML = htmlContent
        } catch (e) {
          infoPanel.innerText = rawInfo
        }
      }
      requestUpdate()
    })
    tile.addEventListener("mouseleave", function () {
      currentRoom = null
      if (infoPanel) {
        infoPanel.innerHTML = "Hover over a room to view details."
      }
      requestUpdate()
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

function worldToScreen(x, y) {
  return {
    x: x * scale + originX,
    y: y * scale + originY,
  }
}

function updateTransform() {
  if (!needsUpdate) return
  panLayer.style.transform = `translate(${originX}px, ${originY}px)`
  grid.style.transform = `scale(${scale})`
  needsUpdate = false
}

function drawArrow(route, solid) {
  if (!route || !route.d) return

  const nums = route.d
  if (nums.length < 6) return

  let a, b, c
  a = worldToScreen(nums[0], nums[1])
  b = worldToScreen(nums[2], nums[3])
  c = worldToScreen(nums[4], nums[5])

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

function redrawCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  if (currentRoom) {
    ctx.lineDashOffset = -dashOffset
    dashOffset += 0.4

    const routes = ROUTES_DATA[currentRoom] || []
    routes.forEach((route) => drawArrow(route))
  }

  window.PATH_ROUTES.forEach((route) =>
    drawArrow(route, !route.isWarp),
  )
}

function requestUpdate() {
  if (!needsUpdate) {
    needsUpdate = true
    requestAnimationFrame(() => {
      updateTransform()
      redrawCanvas()
    })
  }
}

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
  requestUpdate()
})

window.addEventListener("mouseup", () => {
  isPanning = false
  viewport.style.cursor = "grab"
})

// --- MOUSE ZOOM ---
viewport.addEventListener(
  "wheel",
  (e) => {
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
    updateTileBackgrounds()
    requestUpdate()
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
  requestUpdate()
}

window.addEventListener("DOMContentLoaded", () => {
  centerMap()
  updateTileBackgrounds()
  viewport.addEventListener(
    "dblclick",
    (e) => {
      if (localStorage.debug != "true") return
      e.preventDefault()
      e.stopPropagation()
      e.stopImmediatePropagation()
      if (
        e.target?.parentElement?.classList?.contains?.("tile-wrapper")
      ) {
        let [an, ae] = e.target.parentElement.dataset.room.split("_")
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
    redrawCanvas()
  }
}, 30)
