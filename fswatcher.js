const fs = require("fs")
const path = require("path")
const puppeteer = require("puppeteer")
const { Jimp } = require("jimp")

const TARGET_URL = "http://127.0.0.1:8000/MathQuest/play.html"
const WATCH_FILE = "./MQ2Files/loadChar.php"
const DEST_DIR = "./map"
const EXITS_JSON_PATH = "./exits.json"

// Helper to load the raw exits structure safely
function loadExitsRaw() {
  try {
    if (fs.existsSync(EXITS_JSON_PATH)) {
      return JSON.parse(fs.readFileSync(EXITS_JSON_PATH, "utf8"))
    }
  } catch (err) {
    console.warn(
      "[-] Failed to read exits.json, starting with empty baseline:",
      err.message,
    )
  }
  return { edges: [] }
}

// Helper to save the raw exits structure back to file
function saveExitsRaw(data) {
  try {
    fs.writeFileSync(
      EXITS_JSON_PATH,
      JSON.stringify(data, null, 2),
      "utf8",
    )
    console.log(
      `[+] Successfully wrote updates back to ${EXITS_JSON_PATH}`,
    )
  } catch (err) {
    console.error("[-] Error writing to exits.json:", err.message)
  }
}

function waitForFileChange(filePath) {
  return new Promise((resolve) => {
    const watcher = fs.watch(filePath, (eventType) => {
      if (eventType === "change") {
        watcher.close()
        resolve()
      }
    })
  })
}

async function runAutomation() {
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
      return
    }

    if (!fs.existsSync(path.dirname(WATCH_FILE))) {
      fs.mkdirSync(path.dirname(WATCH_FILE), { recursive: true })
    }
    if (!fs.existsSync(WATCH_FILE)) {
      fs.writeFileSync(WATCH_FILE, "")
    }

    await page.exposeFunction(
      "nodeHandleTileProcessing",
      async () => {
        try {
          const coords = await page.evaluate(() => {
            if (typeof player !== "undefined") {
              return { east: player.east, north: player.north }
            }
            return null
          })

          if (
            !coords ||
            coords.east === undefined ||
            coords.north === undefined
          ) {
            console.log("[-] Valid player coordinates not found.")
            return false
          }

          // Fresh load of the database array to handle in-flight modifications
          const rawJsonData = loadExitsRaw()
          const edgesArray =
            Array.isArray(rawJsonData) ? rawJsonData : (
              rawJsonData.edges || []
            )

          // Search for an existing record matching the origin coordinates
          const dbEntry = edgesArray.find(
            (edge) =>
              edge.origin &&
              Number(edge.origin.north) === Number(coords.north) &&
              Number(edge.origin.east) === Number(coords.east),
          )

          if (dbEntry && dbEntry.exits) {
            console.log(
              `[*] Match found in exits.json for [N: ${coords.north}, E: ${coords.east}]. Processing tile snapshot...`,
            )
          } else {
            console.log(
              `[*] No exit data found for [N: ${coords.north}, E: ${coords.east}]. Pausing loop execution...`,
            )
            console.log(
              `[*] Waiting for updates on tracking registry: ${WATCH_FILE}`,
            )

            await waitForFileChange(WATCH_FILE)
            console.log(
              "[+] Change detected! Reading runtime 'exits' property from browser context...",
            )

            // Grab the live 'exits' object from the game environment page
            const liveExits = await page.evaluate(() => {
              return typeof exits !== "undefined" ? exits : null
            })

            if (liveExits && Object.keys(liveExits).length > 0) {
              if (dbEntry) {
                // Exact coordinate match found: merge or write the exits sub-key
                dbEntry.exits = liveExits
                console.log(
                  `[+] Appended new exits key to matching origin item inside JSON matrix.`,
                )
              } else {
                // No matching origin found: create a fallback edge entry shell so data isn't dropped
                const newEdge = {
                  id: `edge:manual:${coords.north}_${coords.east}`,
                  mechanism: "edge",
                  direction: "unknown",
                  origin: { north: coords.north, east: coords.east },
                  dest: null,
                  exits: liveExits,
                }
                edgesArray.push(newEdge)
                console.log(
                  `[+] Created brand new entry structure inside JSON array for missing coordinate origin.`,
                )
              }

              // Re-wrap and save changes right back to the file system
              const payloadToSave =
                Array.isArray(rawJsonData) ? edgesArray : (
                  { ...rawJsonData, edges: edgesArray }
                )
              saveExitsRaw(payloadToSave)
            } else {
              console.log(
                "[-] Browser window variable 'exits' was empty or missing. Skipping JSON file update.",
              )
            }
          }

          // --- Screenshot and Trimming Segment ---
          const destFileName = `${coords.east},${coords.north}.jpg`
          const destPath = path.join(DEST_DIR, destFileName)

          if (!fs.existsSync(destPath)) {
            const canvas = await page.$("canvas")
            if (!canvas) {
              console.error(
                "[-] Canvas element not found on target interface context.",
              )
              return false
            }

            const screenshotBuffer = await canvas.screenshot({
              type: "png",
            })
            const image = await Jimp.read(screenshotBuffer)
            const width = image.bitmap.width
            const height = image.bitmap.height

            let topTrim = 40
            let rightTrim = width - 180
            const leftTrim = 1

            const finalWidth = rightTrim - leftTrim
            const finalHeight = height - topTrim

            if (finalWidth > 0 && finalHeight > 0) {
              image.crop({
                x: leftTrim,
                y: topTrim,
                w: finalWidth,
                h: finalHeight,
              })
              if (!fs.existsSync(DEST_DIR)) {
                fs.mkdirSync(DEST_DIR, { recursive: true })
              }
              await image.write(destPath)
              console.log(`[+] Saved: ${destFileName}`)
            }
          }

          // Clear out tracking variables before advancing positions
          await page.evaluate(() => {
            if (typeof exits !== "undefined") {
              exits = {}
              console.log(
                "[*] Browser context 'exits' layout storage flushed.",
              )
            }
          })

          return true
        } catch (err) {
          console.error(
            "[-] Engine execution error during handling sequence:",
            err.message,
          )
          return false
        }
      },
    )

    console.log("[*] Injecting grid scanning loop...")

    await page.evaluate(async () => {
      if (typeof positions === "undefined") {
        console.error(
          "Positions array configuration targets not accessible in viewport global scope.",
        )
        return
      }

      for (var [north, east] of positions) {
        player.east = east
        player.north = north

        if (typeof test !== "undefined" && test.newScreen)
          test.newScreen()
        if (typeof saver !== "undefined" && saver.save) saver.save()

        await new Promise((resolve) => setTimeout(resolve, 50))

        const success = await window.nodeHandleTileProcessing()

        if (!success) {
          console.warn(
            `Automation sequence safely terminated at coordinate point: ${east}, ${north}`,
          )
          break
        }
      }
      console.log("[+] Automated parsing sweep operations complete!")
    })
  } catch (error) {
    console.error("[-] System Exception Fault:", error.message)
  }
}

runAutomation()
