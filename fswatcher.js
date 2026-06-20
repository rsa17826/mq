const fs = require("fs")

const EXITS_JSON_PATH = "./exits.json"

// Layout Scale Constants
const CANVAS_WIDTH = 624
const CANVAS_HEIGHT = 493

const BLOCK_COLUMNS = 14 // X-Axis
const BLOCK_ROWS = 11    // Y-Axis

// Calculate dimensions of a single tile block in pixels
const BLOCK_WIDTH_PX = CANVAS_WIDTH / BLOCK_COLUMNS   // 624 / 14 = 44.57px
const BLOCK_HEIGHT_PX = CANVAS_HEIGHT / BLOCK_ROWS   // 493 / 11 = 44.81px

/**
 * Converts a pixel position along an axis into its block coordinate,
 * rounding to the absolute center index of that block.
 */
function pxToBlockCenter(pxValue, blockPxSize) {
  // Determine raw floating-point block index placement
  const rawBlockIndex = pxValue / blockPxSize

  // Floor it to find the base block coordinate, then add 0.5 to target the center
  return Math.floor(rawBlockIndex) + 0.5
}

function convertExitsDatabase() {
  if (!fs.existsSync(EXITS_JSON_PATH)) {
    console.error(`[-] Source file not found at: ${EXITS_JSON_PATH}`)
    return
  }

  try {
    const rawData = JSON.parse(fs.readFileSync(EXITS_JSON_PATH, "utf8"))
    const isArrayFormat = Array.isArray(rawData)
    const edgesArray = isArrayFormat ? rawData : (rawData.edges || [])

    let processedCount = 0

    edgesArray.forEach((edge) => {
      if (!edge.exits) return

      processedCount++
      const exits = edge.exits

      // 1. Process horizontal offsets (West & East map bounds use Y dimensions)
      if (exits.west) {
        if (exits.west.top !== null) exits.west.top = pxToBlockCenter(exits.west.top, BLOCK_HEIGHT_PX)
        if (exits.west.bottom !== null) exits.west.bottom = pxToBlockCenter(exits.west.bottom, BLOCK_HEIGHT_PX)
      }
      if (exits.east) {
        if (exits.east.top !== null) exits.east.top = pxToBlockCenter(exits.east.top, BLOCK_HEIGHT_PX)
        if (exits.east.bottom !== null) exits.east.bottom = pxToBlockCenter(exits.east.bottom, BLOCK_HEIGHT_PX)
      }

      // 2. Process vertical offsets (North & South map bounds use X dimensions)
      if (exits.north) {
        if (exits.north.left !== null) exits.north.left = pxToBlockCenter(exits.north.left, BLOCK_WIDTH_PX)
        if (exits.north.right !== null) exits.north.right = pxToBlockCenter(exits.north.right, BLOCK_WIDTH_PX)
      }
      if (exits.south) {
        if (exits.south.left !== null) exits.south.left = pxToBlockCenter(exits.south.left, BLOCK_WIDTH_PX)
        if (exits.south.right !== null) exits.south.right = pxToBlockCenter(exits.south.right, BLOCK_WIDTH_PX)
      }
    })

    // Prepare payload preserving original document structure
    const updatedPayload = isArrayFormat ? edgesArray : { ...rawData, edges: edgesArray }

    // Write translated map data back to storage
    fs.writeFileSync(EXITS_JSON_PATH, JSON.stringify(updatedPayload, null, 2), "utf8")
    console.log(`[+] Complete! Transformed exit parameters across ${processedCount} edge items into block coordinates.`)

  } catch (error) {
    console.error("[-] Conversion pipeline failure error details:", error.message)
  }
}

// Execute translation routine
convertExitsDatabase()