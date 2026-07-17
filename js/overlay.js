function rerange(val, low1, high1, low2, high2) {
  return ((val - low1) / (high1 - low1)) * (high2 - low2) + low2
}
const overlayCanvas = document.querySelector("#overlayCanvas")
var overlayCtx = overlayCanvas.getContext("2d")
const mixCache = {}
function mix(color1, color2) {
  if (!color1) return color2
  if (!color2) return color1
  if (mixCache[`${color1}/${color2}`]) {
    return mixCache[`${color1}/${color2}`]
  }
  // Helper to parse HSL, Hex, or RGB strings into an {r, g, b, a} object
  function parseToRgba(cssString) {
    cssString = cssString.trim()

    // 1. Match HSL/HSLA strings
    var hslMatches = cssString.match(
      /hsla?\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*(?:,\s*([\d.]+)%?\s*)?\)/i,
    )
    if (hslMatches) {
      var h = parseFloat(hslMatches[1])
      var s = parseFloat(hslMatches[2]) / 100
      var l = parseFloat(hslMatches[3]) / 100
      var a =
        hslMatches[4] !== undefined ? parseFloat(hslMatches[4]) : 1
      if (a > 1) a /= 100 // Normalize "60%" or "60" to 0.6

      // Convert HSL to RGB
      var c = (1 - Math.abs(2 * l - 1)) * s
      var x = c * (1 - Math.abs(((h / 60) % 2) - 1))
      var m = l - c / 2
      var r = 0,
        g = 0,
        b = 0

      if (0 <= h && h < 60) {
        r = c
        g = x
        b = 0
      } else if (60 <= h && h < 120) {
        r = x
        g = c
        b = 0
      } else if (120 <= h && h < 180) {
        r = 0
        g = c
        b = x
      } else if (180 <= h && h < 240) {
        r = 0
        g = x
        b = c
      } else if (240 <= h && h < 300) {
        r = x
        g = 0
        b = c
      } else if (300 <= h && h < 360) {
        r = c
        g = 0
        b = x
      }

      return (mixCache[`${color1}/${color2}`] = {
        r: Math.round((r + m) * 255),
        g: Math.round((g + m) * 255),
        b: Math.round((b + m) * 255),
        a: a,
      })
    }

    // 2. Match Hex strings (e.g., #1157, #ff0000)
    if (cssString.startsWith("#")) {
      var hex = cssString.substring(1)
      var r,
        g,
        b,
        a = 1

      if (hex.length === 3 || hex.length === 4) {
        r = parseInt(hex[0] + hex[0], 16)
        g = parseInt(hex[1] + hex[1], 16)
        b = parseInt(hex[2] + hex[2], 16)
        if (hex.length === 4) a = parseInt(hex[3] + hex[3], 16) / 255
      } else if (hex.length === 6 || hex.length === 8) {
        r = parseInt(hex.substring(0, 2), 16)
        g = parseInt(hex.substring(2, 4), 16)
        b = parseInt(hex.substring(4, 6), 16)
        if (hex.length === 8)
          a = parseInt(hex.substring(6, 8), 16) / 255
      }
      return { r: r, g: g, b: b, a: a }
    }

    // 3. Match raw RGB/RGBA strings (for recursive mixtures)
    var rgbaMatches = cssString.match(
      /rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)%?\s*)?\)/i,
    )
    if (rgbaMatches) {
      var a =
        rgbaMatches[4] !== undefined ? parseFloat(rgbaMatches[4]) : 1
      if (a > 1) a /= 100
      return (mixCache[`${color1}/${color2}`] = {
        r: parseInt(rgbaMatches[1]),
        g: parseInt(rgbaMatches[2]),
        b: parseInt(rgbaMatches[3]),
        a: a,
      })
    }

    return (mixCache[`${color1}/${color2}`] = {
      r: 0,
      g: 0,
      b: 0,
      a: 1,
    }) // Fallback
  }

  var c1 = parseToRgba(color1) // Existing background layer
  var c2 = parseToRgba(color2) // New incoming layer drawn on top

  // Standard Source-Over Alpha Blending Formula
  var out_a = c2.a + c1.a * (1 - c2.a)
  if (out_a === 0) return "rgba(0,0,0,0)"

  var out_r = Math.round(
    (c2.r * c2.a + c1.r * c1.a * (1 - c2.a)) / out_a,
  )
  var out_g = Math.round(
    (c2.g * c2.a + c1.g * c1.a * (1 - c2.a)) / out_a,
  )
  var out_b = Math.round(
    (c2.b * c2.a + c1.b * c1.a * (1 - c2.a)) / out_a,
  )

  // Canvas context accept rgba() strings natively
  return (mixCache[`${color1}/${color2}`] =
    "rgba(" +
    out_r +
    ", " +
    out_g +
    ", " +
    out_b +
    ", " +
    out_a.toFixed(2) +
    ")")
}
function customDrawLoop() {
  // 1. Clear the frame
  overlayCtx.clearRect(
    0,
    0,
    overlayCanvas.width,
    overlayCanvas.height,
  )

  if (!window.player) {
    return
  }
  // 1. Define the size of each checkerboard tile
  var tileSize = 50 // Pixels per tile

  // Helper function to check if a specific grid cell (col, row) is an exit tile
  function getExitColor(roomExits, col, row) {
    // Convert our bottom-up canvas row (0 at bottom, 10 at top)
    // to the top-down row index (0 at top, 10 at bottom) used by the data generator
    var topDownRow = 10 - row
    var color = null
    for (var i = 0; i < roomExits.length; i++) {
      var exit = roomExits[i]

      if (exit.side === "warp") {
        if (col == exit.x && row == exit.y) {
          color = mix(color, exit.color)
        }
      }
      if (exit.side === "west" && col === 0) {
        if (topDownRow >= exit.top && topDownRow <= exit.bottom) {
          color = mix(color, exit.color)
        }
      }
      if (exit.side === "east" && col === 13) {
        // 14 columns total (0 to 13)
        if (topDownRow >= exit.top && topDownRow <= exit.bottom) {
          color = mix(color, exit.color)
        }
      }
      if (exit.side === "north" && row === 10) {
        // Top row
        if (col >= exit.left && col <= exit.right) {
          color = mix(color, exit.color)
        }
      }
      if (exit.side === "south" && row === 0) {
        // Bottom row
        if (col >= exit.left && col <= exit.right) {
          color = mix(color, exit.color)
        }
      }
    }
    return color
  }

  function drawExits(room) {
    for (var row = 0; row < 11; row++) {
      for (var col = 0; col < 14; col++) {
        // Check if this tile is an exit
        var exitColor = null
        if (localStorage.renderExits == "true")
          exitColor = mix(exitColor, getExitColor(room, col, row))

        if (localStorage.renderCheckerboard == "true")
          if ((row + col) % 2 === 0) {
            exitColor = mix(exitColor, "#FFFFFF10") // Light overlay instead of skipping entirely
          } else {
            exitColor = mix(exitColor, "#00000050") // Transparent black tile
          }
        if (!exitColor) {
          continue
        }
        overlayCtx.fillStyle = exitColor // Render with the designated exit color

        // Calculate X coordinate (normal math going right)
        var x = col * tileSize

        // Calculate Y coordinate (reverse math starting from bottom-left)
        var y = overlayCanvas.height - tileSize - row * tileSize

        // Draw the tile
        overlayCtx.fillRect(x, y, tileSize, tileSize)
      }
    }
  }

  // Draws the map.js path-to-target arrow (see map.js's PATH_ROUTES),
  // but reprojected onto this room's slice of the checkerboard instead
  // of the whole overview map. The checkerboard covers the full 14x11
  // room grid (tileSize px per block) flush against the bottom of the
  // canvas, so a point that sits at fraction (fx, fy) across the room's
  // map tile lands at the *same relative spot* here.
  var PF_DIR_SCREEN_VECTOR = {
    north: [0, -1],
    south: [0, 1],
    east: [1, 0],
    west: [-1, 0],
  }

  function drawOverlayArrow(a, b) {
    var angle = Math.atan2(b.y - a.y, b.x - a.x)
    var arrowSize = 14

    overlayCtx.beginPath()
    overlayCtx.moveTo(a.x, a.y)
    overlayCtx.lineTo(b.x, b.y)
    overlayCtx.strokeStyle = "#39ff14"
    overlayCtx.lineWidth = 5
    overlayCtx.lineCap = "round"
    overlayCtx.setLineDash([])
    overlayCtx.stroke()

    overlayCtx.beginPath()
    overlayCtx.moveTo(b.x, b.y)
    overlayCtx.lineTo(
      b.x - arrowSize * Math.cos(angle - 0.35),
      b.y - arrowSize * Math.sin(angle - 0.35),
    )
    overlayCtx.lineTo(
      b.x - arrowSize * Math.cos(angle + 0.35),
      b.y - arrowSize * Math.sin(angle + 0.35),
    )
    overlayCtx.closePath()
    overlayCtx.fillStyle = mix("#39ff14", "#00f2")
    overlayCtx.fill()
  }

  function drawRoomPathArrow() {
    // map.js exposes these; if it hasn't loaded (or there's no route
    // selected on the map), there's nothing to draw.
    if (!window.pfWorldPointToRoomFraction) return
    var routes = window.PATH_ROUTES
    if (!routes || !routes.length) return

    var roomKey = `${window.player.north}_${window.player.east}`
    var gridWidth = 14 * tileSize
    var gridHeight = 11 * tileSize
    var gridTop = overlayCanvas.height - gridHeight
    var stubLength = tileSize * 0.8

    function toOverlayPoint(point, forRoom) {
      var frac = window.pfWorldPointToRoomFraction(forRoom, point)
      if (!frac) return null
      return {
        x: frac.fx * gridWidth,
        y: gridTop + frac.fy * gridHeight,
      }
    }

    routes.forEach(function (route) {
      var fromHere = route.fromRoom === roomKey
      var toHere = route.toRoom === roomKey
      if (!fromHere && !toHere) return

      var fromPt =
        fromHere ? toOverlayPoint(route.fromPoint, roomKey) : null
      var toPt =
        toHere ? toOverlayPoint(route.toPoint, roomKey) : null

      if (fromPt && toPt) {
        // Both ends of this hop are in the room the player is standing
        // in (an in-room move) -- draw it exactly as it appears on the
        // overview map, just rescaled to this room's slice of the grid.
        drawOverlayArrow(fromPt, toPt)
        return
      }

      // Only one end of this hop is in the current room -- the other
      // end is elsewhere on the map, so just point toward the exit.
      if (fromPt) {
        var vec = PF_DIR_SCREEN_VECTOR[route.fromDir] || [0, 0]
        // TODO - make show warp dest location and name and work
        if (!route.fromDir) {
          overlayCtx.strokeStyle = "#000"
          overlayCtx.lineJoin = "round"
          overlayCtx.lineWidth = 3 // Controls the thickness of the outline
          overlayCtx.strokeText(owo(route.toRoom), 50, 100)
          overlayCtx.fillStyle = "#ddd"
          overlayCtx.fillText(owo(route.toRoom), 50, 100)
        }
        drawOverlayArrow(fromPt, {
          x: fromPt.x + vec[0] * (stubLength / 1.6),
          y: fromPt.y + vec[1] * (stubLength / 1.6),
        })
      } else if (toPt) {
        var vec2 = PF_DIR_SCREEN_VECTOR[route.toDir] || [0, 0]
        drawOverlayArrow(
          {
            x: toPt.x - vec2[0] * -(stubLength / 1.6),
            y: toPt.y - vec2[1] * -(stubLength / 1.6),
          },
          toPt,
        )
      }
    })
  }
  // Sample multi-line coordinate text setup
  var coordString = ""
  if (
    localStorage.renderExits == "true" ||
    localStorage.renderCheckerboard == "true"
  )
    drawExits(
      EXITS_DATA[`${window.player.north}_${window.player.east}`] ||
        [],
    )

  drawRoomPathArrow()

  coordString =
    localStorage.showPlayerPos == "true" ?
      `
            SCREEN: ${window.player.north}_${window.player.east}
            POS: ${Math.round(window.player.x)} ${Math.round(window.player.y)}
            `
    : ""
  coordString += window.extraData?.() ?? ""
  overlayCtx.font = '36px "Booter - Zero Zero"'

  // Clean the text array up
  var allText = coordString.trim().split("\n")
  if (coordString.trim() === "") allText = [] // Handle empty text gracefully

  // 3. Define layout parameters
  var lineHeight = 30 // Distance between your rows of text
  var baseBottomPadding = 20 // Margin from the bottom boundary line

  // --- PROGRESS BAR CONFIGURATION ---
  // Change these values or bind them to your player stats (e.g., window.player.hp / window.player.maxHp)

  // 4. Draw lines calculating offsets dynamically
  var totalTextHeight = allText.length * lineHeight

  for (var i = 0; i < allText.length; i++) {
    var text = allText[i].trim()

    // Measure current line width so right-alignment holds true
    var textWidth = overlayCtx.measureText(text).width
    var x = overlayCanvas.width - textWidth - 20

    var y =
      overlayCanvas.height -
      baseBottomPadding -
      (allText.length - 1 - i) * lineHeight

    overlayCtx.strokeStyle = "#000"
    overlayCtx.lineJoin = "round"
    overlayCtx.lineWidth = 3 // Controls the thickness of the outline
    overlayCtx.strokeText(owo(text), x, y)
    overlayCtx.fillStyle = "#ddd"
    overlayCtx.fillText(owo(text), x, y)
  }
  // render chest hints
  {
    if (localStorage.showVanillaItems != "true") {
      for (var [
        _color,
        {
          data: itemNames,
          position: { x: _x, y: _y },
          elem,
        },
      ] of Object.entries(
        window.chestedItemInfo[`${manager.north}_${manager.east}`] ??
          {},
      )) {
        if (elem.__visible) {
          var lines = itemNames.map(owo)

          overlayCtx.strokeStyle = "#000"
          overlayCtx.lineJoin = "round"
          overlayCtx.lineWidth = 3
          overlayCtx.fillStyle = "#ddd"

          lines.forEach(function (line, index) {
            var currentY = _y + index * lineHeight
            var w = overlayCtx.measureText(line).width
            overlayCtx.strokeText(line, Math.max(0, _x - w / 2), currentY)
            overlayCtx.fillText(line, Math.max(0, _x - w / 2), currentY)
          })
        }
      }
    }
  }
  var currentOffsetY = totalTextHeight - 10
  var progressValue = 0
  var maxProg = 0
  if (window.ap?.slotData) {
    var prog = 0
    if (ap.slotData.final_boss) {
      maxProg += 23
      prog += Math.min(manager.quest[Enum.Quest.gTree], 23)
    }
    if (ap.slotData?.all_quests_maxed) {
      prog += Object.entries(ap.slotData.maxQuests).reduce(
        (a, [k, v]) => a + Math.min(v, manager.quest[Enum.Quest[k]]),
        0,
      )
      maxProg += Object.values(ap.slotData.maxQuests).reduce(
        (a, v) => a + v,
        0,
      )
    }
    progressValue = rerange(prog, 0, maxProg, 0, 1)
    newBar(
      progressValue,
      155 + 30,
      12,
      10,
      `progress: ${Math.floor(progressValue * 100)}%`,
    )
  }
  var progressValue = 0
  var maxProg = 0
  if (window.ap?.slotData) {
    progressValue = rerange(
      ap.checkedLocations.length,
      0,
      ap.missingLocations.length + ap.checkedLocations.length,
      0,
      1,
    )
    newBar(
      progressValue,
      155 + 30,
      12,
      10,
      `checks: ${Math.floor(progressValue * 100)}%`,
    )
  }

  function newBar(
    progressValue,
    barWidth,
    barHeight,
    barPadding,
    barText,
  ) {
    // Add padding first
    currentOffsetY += barPadding

    // Base coordinates for the entire component container
    var containerX = overlayCanvas.width - barWidth - 5
    var barY =
      overlayCanvas.height -
      baseBottomPadding -
      currentOffsetY -
      barHeight

    var dynamicBarWidth = barWidth
    var textWidth = 0

    // If text is provided, measure it and adjust the bar's width
    if (barText) {
      overlayCtx.font = '28px "Booter - Zero Zero"' // Font for the bar text
      textWidth = overlayCtx.measureText(barText).width
      var textSpacing = 8 // Space between the bar and the text

      // Shrink the bar width to make room for the text and spacing
      dynamicBarWidth = Math.max(
        0,
        barWidth - textWidth - textSpacing,
      )
    }

    // 1. Draw Background / Border Outline for the bar
    if (dynamicBarWidth > 0) {
      overlayCtx.fillStyle = "#000"
      overlayCtx.fillRect(
        containerX - 2,
        barY - 2,
        dynamicBarWidth + 4,
        barHeight + 4,
      ) // Outer black border

      overlayCtx.fillStyle = "#444"
      overlayCtx.fillRect(
        containerX,
        barY,
        dynamicBarWidth,
        barHeight,
      ) // Dark background fill

      // 2. Draw Foreground (The actual progress)
      overlayCtx.fillStyle = "#00ffcc" // Cyan/Green progress color
      overlayCtx.fillRect(
        containerX,
        barY,
        dynamicBarWidth * progressValue,
        barHeight,
      )
    }

    // 3. Draw the text on the far right of the total barWidth area
    if (barText) {
      var textX = overlayCanvas.width - textWidth - 5
      // Vertically center text relative to the bar height
      var textY = barY + barHeight / 2 + 5

      overlayCtx.strokeStyle = "#000"
      overlayCtx.lineJoin = "round"
      overlayCtx.lineWidth = 3
      overlayCtx.strokeText(owo(barText), textX, textY)
      overlayCtx.fillStyle = "#ddd"
      overlayCtx.fillText(owo(barText), textX, textY)
    }

    // Shift the offset up by the height of this bar so the next bar sits above it
    currentOffsetY += barHeight
  }
  requestAnimationFrame(customDrawLoop)
}
customDrawLoop()
