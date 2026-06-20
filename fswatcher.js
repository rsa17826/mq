const fs = require("fs")
const puppeteer = require("puppeteer")
const { exec } = require("child_process") // Added to execute system commands
const TARGET_URL = "http://127.0.0.1:8000/MathQuest/play.html"
const GEOMETRY_FILE = "./room_geometry.json"

// Function to update room completion status in JSON file
function markRoomAsComplete(east, north) {
  if (!fs.existsSync(GEOMETRY_FILE)) {
    console.error(
      `[-] ${GEOMETRY_FILE} does not exist. Cannot mark complete.`,
    )
    return
  }

  try {
    const fileData = fs.readFileSync(GEOMETRY_FILE, "utf8")
    let rooms = JSON.parse(fileData)

    let updated = false
    rooms = rooms.map((room) => {
      if (room.east === east && room.north === north) {
        if (!room.complete) {
          room.complete = true
          updated = true
        }
      }
      return room
    })

    if (updated) {
      fs.writeFileSync(
        GEOMETRY_FILE,
        JSON.stringify(rooms, null, 2),
        "utf8",
      )
      console.log(
        `[+] Marked room (${north}, ${east}) as complete in ${GEOMETRY_FILE}`,
      )
      console.log("[*] Running python map/genGrid.py...")

      exec("python map/genGrid.py", (error, stdout, stderr) => {
        if (error) {
          console.error(
            `[-] Python execution error: ${error.message}`,
          )
          return
        }
        if (stderr) {
          console.error(`[-] Python stderr: ${stderr}`)
          return
        }
        console.log(`[+] Python stdout:\n${stdout.trim()}`)
      })
    }
  } catch (error) {
    console.error(
      "[-] Error updating room geometry JSON:",
      error.message,
    )
  }
}

async function startTracking() {
  let browser
  try {
    browser = await puppeteer.connect({
      browserURL: "http://127.0.0.1:9222",
      defaultViewport: null,
    })

    const pages = await browser.pages()
    const page = pages.find((p) => p.url().includes(TARGET_URL))

    if (!page) {
      console.error(`[-] Could not find tab: ${TARGET_URL}`)
      if (browser) await browser.disconnect()
      return
    }

    console.log(
      `[*] Successfully attached to game tab. Watching player coordinates...`,
    )

    // Initialize tracking variables
    let lastCoords = { east: null, north: null }

    // Loop to continuously monitor player movement in the browser context
    while (true) {
      const currentCoords = await page.evaluate(() => {
        if (
          typeof player !== "undefined" &&
          player.east !== undefined &&
          player.north !== undefined
        ) {
          return { east: player.east, north: player.north }
        }
        return null
      })

      if (currentCoords) {
        // If the coordinates changed from the last iteration, execute automation logic
        if (
          currentCoords.east !== lastCoords.east ||
          currentCoords.north !== lastCoords.north
        ) {
          console.log(
            `[*] Position change detected: (${currentCoords.north}, ${currentCoords.east})`,
          )
          lastCoords = currentCoords

          markRoomAsComplete(currentCoords.east, currentCoords.north)
        }
      }

      // Poll every 200ms to preserve performance
      await new Promise((resolve) => setTimeout(resolve, 200))
    }
  } catch (error) {
    console.error("[-] Connection or runtime error:", error.message)
    if (browser) await browser.disconnect()
  }
}

startTracking()
