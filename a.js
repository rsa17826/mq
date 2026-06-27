const puppeteer = require("puppeteer")
const fs = require("fs")
const path = require("path")
const { execSync, exec } = require("child_process")

// Configuration
const DEBUG_URL = "http://127.0.0.1:9222" // Your Chrome debugging port
const TARGET_PAGE_URL = "http://127.0.0.1:1533/MathQuest/play.html"
const BASE_FILE_PATH =
  path.expandHome ?
    path.expandHome("~/projects/mq/MathQuest/MathQuest.base.js")
  : `${process.env.HOME}/projects/mq/MathQuest/MathQuest.base.js`
const FINAL_FILE_PATH = BASE_FILE_PATH.replace(
  "MathQuest.base.js",
  "MathQuest.js",
)

// Helper function to pause execution and wait for file changes
function waitForFileSave(filePath) {
  return new Promise((resolve) => {
    console.log(`Waiting for changes to be saved in Codium...`)
    const watcher = fs.watch(filePath, (eventType) => {
      if (eventType === "change") {
        console.log(`File save detected.`)
        watcher.close()
        resolve()
      }
    })
  })
}
var min = 1000
var start = 111200
var len = 209
// Helper to insert a line into a specific file at a specific line number
function insertLineInFile(filePath, lineNumber, textToInsert) {
  const fileContent = fs.readFileSync(filePath, "utf8")
  const lines = fileContent.split("\n")

  // Adjusting for 0-indexed array vs 1-indexed line numbers
  lines.splice(lineNumber - 1, 0, textToInsert)

  fs.writeFileSync(filePath, lines.join("\n"), "utf8")
}
async function main() {
  let browser
  try {
    // 1. Connect to the existing browser session
    browser = await puppeteer.connect({
      browserURL: DEBUG_URL,
      defaultViewport: null,
    })
    const pages = await browser.pages()

    // Find the target tab
    const page = pages.find((p) => p.url().includes(TARGET_PAGE_URL))
    if (!page) {
      console.error(
        `Could not find a tab with URL: ${TARGET_PAGE_URL}`,
      )
      return
    }
    console.log(
      "🚀 Automation loop started. Press Ctrl+C in terminal to stop.",
    )

    // Tracks every original line number where we have successfully inserted a token
    const insertedOriginalLines = []

    // Continuous processing loop
    while (true) {
      // 2. Extract variables from the browser page context
      const pageData = await page.evaluate(() => {
        return {
          north: window.manager ? window.manager.north : null,
          east: window.manager ? window.manager.east : null,
          accessList: window.accessList || {},
        }
      })

      const { north, east, accessList } = pageData
      const currentKey = `${north}_${east}`

      // Check if there are active items to process for the current coordinates
      if (
        accessList[currentKey] &&
        accessList[currentKey].length > 0
      ) {
        console.log(
          `\nFound ${accessList[currentKey].length} items to write for: ${currentKey}`,
        )

        // Sorting ascending ensures predictable behavior within the same batch
        const itemsToProcess = [...accessList[currentKey]].sort(
          (a, b) => a[1] - b[1],
        )

        // Process each item in this coordinate chunk sequentially
        for (const item of itemsToProcess) {
          var [prop, originalLineNumber] = item
          originalLineNumber = Number(originalLineNumber)
          // Calculate offset: count how many previous insertions happened ABOVE this line
          const dynamicOffset = insertedOriginalLines.filter(
            (line) => line < originalLineNumber,
          ).length

          console.log("\n", {
            typeofOriginal: typeof originalLineNumber,
            originalLineNumber: originalLineNumber,
            startValue: start,
            lenValue: len,
            dynamicOffset: dynamicOffset,
          })
          if (originalLineNumber < min) {
            continue
          }
          var adjustedLineNumber = originalLineNumber + dynamicOffset
          const textToWrite = `newItem(${north},${east},'${prop}',)`
          if (adjustedLineNumber > start) {
            adjustedLineNumber -= len
          }
          console.log(
            `Processing: Inserting "${textToWrite}" at adjusted line ${adjustedLineNumber} ` +
              `(Original: ${originalLineNumber}, Active Offset: +${dynamicOffset})`,
          )

          // Write to the base file using the dynamically adjusted line number
          insertLineInFile(
            BASE_FILE_PATH,
            adjustedLineNumber,
            textToWrite,
          )

          // 4. Open VS Codium to the adjusted line number
          console.log(
            `codium --goto "${BASE_FILE_PATH}:${adjustedLineNumber}`,
          )
          // exec(
          //   `codium --goto "${BASE_FILE_PATH}:${adjustedLineNumber}"`,
          //   (err) => {
          //     if (err)
          //       console.error(`Failed to open Codium: ${err.message}`)
          //   },
          // )

          // 5. Wait for the user to manually save the file before moving to the next item
          // await waitForFileSave(BASE_FILE_PATH)
          await new Promise((e) => setTimeout(e, 300))

          // Save this original line location to history for future offset math
          insertedOriginalLines.push(originalLineNumber)
        }

        // 6. Run post-processing commands for this batch
        console.log(
          "Batch complete. Saving state and running compilers...",
        )
        await page.evaluate(() => {
          window.test.save()
        })

        try {
          execSync("python main.py 32 --no-shuffle")
          // execSync(`push adding items to randomize ${currentKey}`)
        } catch (cmdError) {
          console.error(
            "Error executing terminal commands:",
            cmdError.message,
          )
        }

        // 7. Clear out the processed entries from the browser so we don't loop over them again
        await page.evaluate((key) => {
          if (window.accessList && window.accessList[key]) {
            delete window.accessList[key]
          }
        }, currentKey)

        console.log(
          `Done with batch ${currentKey}. Listening for new tokens...`,
        )
      }

      // Poll the browser context every 1 second
      await new Promise((resolve) => setTimeout(resolve, 1000))
    }
  } catch (error) {
    console.error("An error occurred during execution:", error)
  } finally {
    if (browser) {
      await browser.disconnect()
    }
  }
}

main()
