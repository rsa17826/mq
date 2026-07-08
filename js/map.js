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
