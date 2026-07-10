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
// otherwise falls back to plain grid-neighbor connections.
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
let pathGraph = null
let pathGraphSourceSlotData = null

function pfRoomKey(n, e) {
  return `${n}_${e}`
}

function pfAddEdge(graph, from, to, fromDir, fromIdx, toDir, toIdx) {
  if (!graph[from]) graph[from] = []
  graph[from].push({
    from,
    to,
    fromDir,
    fromIdx: Number(fromIdx),
    toDir,
    toIdx: Number(toIdx),
  })
}

function buildPathGraph(slotData) {
  const graph = {}

  if (Array.isArray(slotData.roomData) && slotData.roomData.length) {
    // Entrance-rando-aware: every row is one physical link between two
    // exits. Traversable both ways.
    slotData.roomData.forEach((row) => {
      const [n1, e1, dir1, idx1, n2, e2, dir2, idx2] = row
      const k1 = pfRoomKey(n1, e1)
      const k2 = pfRoomKey(n2, e2)
      pfAddEdge(graph, k1, k2, dir1, idx1, dir2, idx2)
      pfAddEdge(graph, k2, k1, dir2, idx2, dir1, idx1)
    })
    return graph
  }

  // Fallback (vanilla layout): exit N in a direction connects to exit N
  // (same index) in the opposite direction of the neighboring room.
  const rooms = slotData.AP_ENTRANCE_IDS || []
  const byKey = {}
  rooms.forEach((room) => {
    if (room && room.north !== undefined && room.east !== undefined) {
      byKey[pfRoomKey(room.north, room.east)] = room
    }
  })

  rooms.forEach((room) => {
    if (!room || !room.exits) return
    const fromKey = pfRoomKey(room.north, room.east)
    Object.keys(room.exits).forEach((dir) => {
      const list = room.exits[dir]
      if (!Array.isArray(list)) return
      const [dn, de] = PF_DIR_OFFSET[dir] || [0, 0]
      const toKey = pfRoomKey(room.north + dn, room.east + de)
      if (!byKey[toKey]) return
      list.forEach((_, idx) => {
        pfAddEdge(
          graph,
          fromKey,
          toKey,
          dir,
          idx,
          PF_OPPOSITE[dir],
          idx,
        )
      })
    })
  })

  return graph
}

function getPathGraph() {
  const slotData = window.ap && window.ap.slotData
  if (!slotData) return null
  if (pathGraph && pathGraphSourceSlotData === slotData)
    return pathGraph
  pathGraph = buildPathGraph(slotData)
  pathGraphSourceSlotData = slotData
  return pathGraph
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

// BFS shortest-path over rooms (one hop = taking an exit).
function pfBfs(graph, startKey) {
  const dist = { [startKey]: 0 }
  const bestEdge = {}
  const allIncoming = {}
  const queue = [startKey]
  let qi = 0

  while (qi < queue.length) {
    const cur = queue[qi++]
    const edges = graph[cur] || []
    for (const edge of edges) {
      if (!allIncoming[edge.to]) allIncoming[edge.to] = []
      allIncoming[edge.to].push(edge)
      if (dist[edge.to] === undefined) {
        dist[edge.to] = dist[cur] + 1
        bestEdge[edge.to] = edge
        queue.push(edge.to)
      }
    }
  }

  return { dist, bestEdge, allIncoming }
}

function pfReconstructPath(bestEdge, targetKey) {
  const path = []
  let cur = targetKey
  while (bestEdge[cur]) {
    const edge = bestEdge[cur]
    path.unshift(edge)
    cur = edge.from
  }
  return path
}

// Path from the player's current room to targetKey. If targetEntrance
// ({dir, idx}) is given, the route ends specifically through that entrance
// (may be a hop longer than the shortest room-to-room path).
function findPathTo(targetKey, targetEntrance) {
  const graph = getPathGraph()
  const startKey = getCurrentRoomKey()
  if (!graph || !startKey) return null
  if (startKey === targetKey && !targetEntrance) return []

  const { dist, bestEdge, allIncoming } = pfBfs(graph, startKey)

  if (!targetEntrance) {
    if (dist[targetKey] === undefined) return null
    return pfReconstructPath(bestEdge, targetKey)
  }

  const candidates = (allIncoming[targetKey] || []).filter(
    (e) =>
      e.toDir === targetEntrance.dir &&
      e.toIdx === targetEntrance.idx,
  )
  if (!candidates.length) return null

  candidates.sort(
    (a, b) => (dist[a.from] ?? Infinity) - (dist[b.from] ?? Infinity),
  )
  const finalEdge = candidates[0]
  if (dist[finalEdge.from] === undefined) return null

  const pathToSource =
    finalEdge.from === startKey ?
      []
    : pfReconstructPath(bestEdge, finalEdge.from)
  return [...pathToSource, finalEdge]
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

// World/grid pixel point for a room's exit in a given direction. Falls
// back to the middle of that tile edge if exit geometry isn't found.
function pfExitPoint(roomKey, dir, idx) {
  const origin = pfTileOrigin(roomKey)
  if (!origin) return null

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
    const a = pfExitPoint(edge.from, edge.fromDir, edge.fromIdx)
    const b = pfExitPoint(edge.to, edge.toDir, edge.toIdx)
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

function drawArrow(route) {
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
  ctx.lineWidth = 4
  ctx.setLineDash([12, 8])
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
  if (!currentRoom) return

  ctx.lineDashOffset = -dashOffset
  dashOffset += 0.4

  const routes = ROUTES_DATA[currentRoom] || []
  routes.forEach(drawArrow)
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
      if (e.target.classList.contains("tile-wrapper")) {
        let [an, ae] = e.target.dataset.room.split("_")
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
