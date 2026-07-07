const overlayCanvas = document.querySelector("#overlayCanvas")
var overlayCtx = overlayCanvas.getContext("2d")

function customDrawLoop() {
  try {
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
    function mix(color1, color2) {
      if (!color1) return color2
      if (!color2) return color1

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
            hslMatches[4] !== undefined ?
              parseFloat(hslMatches[4])
            : 1
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

          return {
            r: Math.round((r + m) * 255),
            g: Math.round((g + m) * 255),
            b: Math.round((b + m) * 255),
            a: a,
          }
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
            if (hex.length === 4)
              a = parseInt(hex[3] + hex[3], 16) / 255
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
            rgbaMatches[4] !== undefined ?
              parseFloat(rgbaMatches[4])
            : 1
          if (a > 1) a /= 100
          return {
            r: parseInt(rgbaMatches[1]),
            g: parseInt(rgbaMatches[2]),
            b: parseInt(rgbaMatches[3]),
            a: a,
          }
        }

        return { r: 0, g: 0, b: 0, a: 1 } // Fallback
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
      return (
        "rgba(" +
        out_r +
        ", " +
        out_g +
        ", " +
        out_b +
        ", " +
        out_a.toFixed(2) +
        ")"
      )
    }
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
              // Alternate checkerboard background colors for standard non-exit tiles
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

    coordString =
      localStorage.showPlayerPos == "true" ?
        `
            SCREEN: ${window.player.north}_${window.player.east}
            POS: ${Math.round(window.player.x)} ${Math.round(window.player.y)}
            `
      : ""

    overlayCtx.font = "bold 20px sans-serif"

    // Clean the text array up
    var allText = coordString.trim().split("\n")

    // 3. Define layout parameters
    var lineHeight = 24 // Distance between your rows of text
    var baseBottomPadding = 20 // Margin from the bottom boundary line

    // 4. Draw lines calculating offsets dynamically
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
      overlayCtx.strokeText(text, x, y)
      overlayCtx.fillStyle = "#ddd"
      overlayCtx.fillText(text, x, y)
    }
  } catch (e) {
    error(e)
  } finally {
    requestAnimationFrame(customDrawLoop)
  }
}
customDrawLoop()
