const puppeteer = require("puppeteer-core")
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
    browser = await puppeteer.connect({ browserURL: DEBUG_URL })
    const pages = await browser.pages()

    // Find the target tab
    const page = pages.find((p) => p.url().includes(TARGET_PAGE_URL))
    if (!page) {
      console.error(
        `Could not find a tab with URL: ${TARGET_PAGE_URL}`,
      )
      return
    }

    // 2. Extract variables from the browser page context
    const pageData = await page.evaluate(() => {
      return {
        north: window.manager ? window.manager.north : null,
        east: window.manager ? window.manager.east : null,
        accessList: window.accessList || [],
      }
    })

    const { north, east, accessList } = pageData
    console.log(
      `Extracted Data - North: ${north}, East: ${east}, AccessList Length: ${accessList.length}`,
    )

    if (accessList.length === 0) {
      console.log("accessList is empty. No operations to perform.")
      return
    }

    // 3. Process each item in the accessList sequentially
    for (const item of accessList[`${north}_${east}`]) {
      const [prop, lineNumber] = item
      const textToWrite = `newItem(${north},${east},'${prop}',)`

      console.log(
        `Processing: Inserting "${textToWrite}" at line ${lineNumber}`,
      )

      // Write to the base file
      insertLineInFile(BASE_FILE_PATH, lineNumber, textToWrite)

      // 4. Open VS Codium to the specific file and line number
      // Syntax: codium --goto filename:line:column
      exec(
        `codium --goto "${BASE_FILE_PATH}:${lineNumber}"`,
        (err) => {
          if (err)
            console.error(`Failed to open Codium: ${err.message}`)
        },
      )

      // 5. Wait for the user to manually save the file before moving to the next item
      await waitForFileSave(BASE_FILE_PATH)
      await new Promise(e=>setTimeout(e,100))
    }

    // 6. When list is empty, copy MathQuest.base.js to MathQuest.js
    console.log(
      "Access list fully processed. Copying base file to final file...",
    )
    page.evaluate(() => {
      window.test.save()
    })
    execSync("prettier --write --semi=false --print-width=70 --experimental-ternaries=true --tab-width=2  MathQuest/MathQuest.base.js")
    execSync("python main.py 32 --no-shuffle")
    execSync("push adding items to randomize")
    // fs.copyFileSync(BASE_FILE_PATH, FINAL_FILE_PATH)

    // 7. Reload the target page
    console.log("Reloading the browser page...")
    await page.reload({ waitUntil: "load" })
    console.log("Done!")
  } catch (error) {
    console.error("An error occurred during execution:", error)
  } finally {
    if (browser) {
      await browser.disconnect()
    }
  }
}

main()
