const fs = require("fs")
const path = require("path")
const puppeteer = require("puppeteer")
const { Jimp } = require("jimp")

const TARGET_URL = "http://127.0.0.1:8000/MathQuest/play.html"
const DEST_DIR = "./map"

async function runAutomation() {
  let browser
  try {
    // 1. Connect to Chrome
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

    // 2. Expose the save function to the browser context
    // This allows player loop to say "Hey Node, process the current screen and tell me when you're done!"
    await page.exposeFunction("nodeProcessAndSaveScreenshot", async () => {
      try {
        const coords = await page.evaluate(() => {
          if (typeof player !== "undefined") {
            return { east: player.east, north: player.north }
          }
          return null
        })

        if (!coords || coords.east === undefined || coords.north === undefined) {
          console.log("[-] Valid player coordinates not found.")
          return false // Tell browser save failed
        }

        const destFileName = `${coords.north},${coords.east}.jpg`
        const destPath = path.join(DEST_DIR, destFileName)

        if (fs.existsSync(destPath)) {
          console.log(`[-] File already exists at ${destPath}. Skipping processing.`)
          return true // Skip but return true so it advances to the next tile
        }

        const canvas = await page.$("canvas")
        if (!canvas) {
          console.error("[-] Canvas element not found on page.")
          return false
        }

        const screenshotBuffer = await canvas.screenshot({ type: "png" })
        const image = await Jimp.read(screenshotBuffer)
        const width = image.bitmap.width
        const height = image.bitmap.height

        let topTrim = 40
        let rightTrim = width - 180
        const leftTrim = 1

        const finalWidth = rightTrim - leftTrim
        const finalHeight = height - topTrim

        if (finalWidth <= 0 || finalHeight <= 0) {
          console.error("[-] Calculated trim dimensions are invalid.")
          return false
        }

        image.crop({ x: leftTrim, y: topTrim, w: finalWidth, h: finalHeight })

        if (!fs.existsSync(DEST_DIR)) {
          fs.mkdirSync(DEST_DIR, { recursive: true })
        }

        await image.write(destPath)
        console.log(`[+] Saved: ${destFileName}`)
        return true // Success! Tell browser to continue loop
      } catch (err) {
        console.error("[-] Error handling screenshot execution:", err.message)
        return false
      }
    })

    console.log("[*] Injecting grid scraping loop into the browser...")

    // 3. Inject the loop directly into the page execution context
    await page.evaluate(async () => {
      // Replace this array placeholder with your actual generation logic/coordinates variable if needed
      // Assuming 'positions' is already defined on your game window, or we define it here:
      if (typeof positions === 'undefined') {
        console.error("Positions array not defined on page window context.");
        return;
      }

      for (var [north, east] of positions) {
        player.east = east
        player.north = north

        // Let the engine process game state movement
        if (typeof test !== 'undefined' && test.newScreen) test.newScreen();

        // Force engine mechanics to trigger save conditions or updates
        if (typeof saver !== 'undefined' && saver.save) saver.save();

        // Give the game engine a brief moment (e.g., 50ms) to finish re-rendering the graphical tiles
        await new Promise((resolve) => setTimeout(resolve, 50));

        // Wait completely until Node.js finishes writing the cropped tile file
        const success = await window.nodeProcessAndSaveScreenshot();

        if (!success) {
          console.warn(`Stopped loop at coordinate iteration: ${north}, ${east} due to an error.`);
          break;
        }
      }
      console.log("Custom grid automated scanning operations complete!");
    })

  } catch (error) {
    console.error("[-] Runner Exception:", error.message)
  }
}

runAutomation()