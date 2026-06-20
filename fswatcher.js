const fs = require("fs")
const path = require("path")
const puppeteer = require("puppeteer")
const { Jimp } = require("jimp") // Make sure to use modern jimp syntax

const TARGET_URL = "http://127.0.0.1:8000/MathQuest/play.html"
const WATCH_FILE = "./MQ2Files/loadChar.php"
const DEST_DIR = "./map"

// Target background colors in Hex (Jimp reads them as 0xRRGGBBAA)
const TARGET_COLORS = [
  0x212a33ff, // #212A33
  0x111619ff, // #111619
]

// Helper to check if a pixel color matches our target colors (ignoring alpha channel differences)
function isTargetColor(pixelColor) {
  // Mask out alpha channel to compare RGB
  const rgb = pixelColor & 0xffffff00
  return TARGET_COLORS.some((target) => (target & 0xffffff00) === rgb)
}

async function processMapScreenshot() {
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

    // 2. Fetch coordinates
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
      return
    }

    const destFileName = `${coords.east},${coords.north}.jpg`
    const destPath = path.join(DEST_DIR, destFileName)

    // Check if destination file already exists
    if (fs.existsSync(destPath)) {
      console.log(`[-] File already exists at ${destPath}. Skipping.`)
      return
    }

    // 3. Find canvas and capture screenshot buffer
    const canvas = await page.$("canvas")
    if (!canvas) {
      console.error("[-] Canvas element not found on page.")
      return
    }
    const screenshotBuffer = await canvas.screenshot({ type: "png" })

    // 4. Process image trimming with Jimp
    const image = await Jimp.read(screenshotBuffer)
    const width = image.bitmap.width
    const height = image.bitmap.height

    // Determine top trim boundary (scan down from top-middle until target color hit)
    let topTrim = 40

    // Determine right trim boundary (scan left from right-middle until target color hit)
    let rightTrim = width - 180

    // Apply strict 1px trim from left side
    const leftTrim = 1

    // Calculate final dimensions for cropping
    const finalWidth = rightTrim - leftTrim
    const finalHeight = height - topTrim

    if (finalWidth <= 0 || finalHeight <= 0) {
      console.error("[-] Calculated trim dimensions are invalid.")
      return
    }

    // Crop the image
    image.crop({
      x: leftTrim,
      y: topTrim,
      w: finalWidth,
      h: finalHeight,
    })

    // Ensure directory exists and save
    if (!fs.existsSync(DEST_DIR)) {
      fs.mkdirSync(DEST_DIR, { recursive: true })
    }

    await image.write(destPath)
    console.log(`[+] Trimmed canvas screenshot saved to: ${destPath}`)
  } catch (error) {
    console.error("[-] Error running automation:", error.message)
  } finally {
    if (browser) await browser.disconnect()
  }
}

// Watch mechanism with debounce logic
let watchTimeout
console.log(`[*] Watching for changes to ${WATCH_FILE}...`)

if (!fs.existsSync(path.dirname(WATCH_FILE))) {
  fs.mkdirSync(path.dirname(WATCH_FILE), { recursive: true })
}
// Create file if it doesn't exist so fs.watch has something to track
if (!fs.existsSync(WATCH_FILE)) {
  fs.writeFileSync(WATCH_FILE, "")
}

fs.watch(WATCH_FILE, (eventType) => {
  if (eventType === "change") {
    clearTimeout(watchTimeout)
    watchTimeout = setTimeout(processMapScreenshot, 150)
  }
})
