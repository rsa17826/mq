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
let PATH_ROUTES = []
let selectedPathId = null // identifies whatever room/entrance is currently clicked-on, or null

function pfSelectionId(roomKey, entrance) {
  return entrance ?
      `${roomKey}::${entrance.dir}::${entrance.idx}`
    : roomKey
}

// Clicking a tile/entrance shows the route to it; clicking the same one
// again clears the route.
function selectPathTarget(roomKey, entrance) {
  const id = pfSelectionId(roomKey, entrance)
  if (selectedPathId === id) {
    selectedPathId = null
    clearPathRoute()
    return
  }
  selectedPathId = id
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
  const have = window.haveReal || new Set()

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

  return { graph, roomsByKey }
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

// Path from the player's current room to targetKey. If targetEntrance
// ({dir, idx}) is given, the route ends specifically through that entrance
// (may be a hop longer than the shortest room-to-room path). Returns null
// if there's genuinely no valid route with what the player currently has.
function findPathTo(targetKey, targetEntrance) {
  const slotData = window.ap && window.ap.slotData
  const startKey = getCurrentRoomKey()
  if (!slotData || !startKey) return null

  const { graph, roomsByKey } = buildPathGraph(slotData)
  if (!roomsByKey[startKey]) return null

  if (startKey === targetKey && !targetEntrance) return []

  const { dist, bestEdge } = pfBfs(graph, roomsByKey, startKey)

  if (targetEntrance) {
    const targetNode = pfExitNodeKey(
      targetKey,
      targetEntrance.dir,
      targetEntrance.idx,
    )
    if (dist[targetNode] === undefined) return null
    return pfReconstructPath(bestEdge, targetNode)
  }

  // No specific entrance requested: take the closest exit-node belonging
  // to that room that's actually reachable.
  const prefix = `${targetKey}::`
  let bestNode = null
  let bestDist = Infinity
  for (const node of Object.keys(dist)) {
    if (node.startsWith(prefix) && dist[node] < bestDist) {
      bestDist = dist[node]
      bestNode = node
    }
  }
  if (!bestNode) return null
  return pfReconstructPath(bestEdge, bestNode)
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
    })
  }
  return routes
}

// No route found -> PATH_ROUTES ends up empty -> nothing is drawn.
function showPathTo(targetKey, targetEntrance) {
  const path = findPathTo(targetKey, targetEntrance)
  PATH_ROUTES = buildPathRoutes(path)
  requestUpdate()
}

function clearPathRoute() {
  PATH_ROUTES = []
  requestUpdate()
}

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
      selectPathTarget(this.getAttribute("data-room"))
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
        const roomKey = this.getAttribute("data-room")
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
  const arrowSize = 12

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

  ctx.fillStyle = route.color
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

  PATH_ROUTES.forEach((route) => drawArrow(route, true))
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
