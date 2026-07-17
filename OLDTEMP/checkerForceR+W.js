const fs = require("fs")
const readline = require("readline")

async function scanFile(filePath) {
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`)
    return
  }

  const fileStream = fs.createReadStream(filePath)
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  })

  let lineNumber = 0
  const reads = []
  const writes = []

  // Captures both formats: checker.property or checker["property"]
  const anyPattern =
    /\bchecker(?:(\.[a-zA-Z_0-9.]+)|\[['"`]([^'"`]+)['"`]\])/g

  for await (const line of rl) {
    lineNumber++

    const trimmed = line.trim()
    if (trimmed.startsWith("//") || trimmed.startsWith("*")) continue

    let match
    anyPattern.lastIndex = 0

    while ((match = anyPattern.exec(line)) !== null) {
      const propName = match[1] ? match[1].slice(1) : match[2]
      const unifiedKey = `checker["${propName}"]`

      const matchIndex = match.index
      const remainingLine = line
        .slice(matchIndex + match[0].length)
        .trim()

      // Check for any assignment/mutation operator: =, +=, -=, *=, /=, or increment/decrement ++, --
      const isWrite =
        /^(\+=|-=|\*=|\/=\||%=|=(?!=))/.test(remainingLine) ||
        remainingLine.startsWith("++") ||
        remainingLine.startsWith("--")

      if (isWrite) {
        writes.push({ item: unifiedKey, line: lineNumber })
      } else {
        reads.push({ item: unifiedKey, line: lineNumber })
      }
    }
  }

  const allItems = new Set([
    ...reads.map((r) => r.item),
    ...writes.map((w) => w.item),
  ])

  allItems.forEach((item) => {
    const itemReads = reads
      .filter((r) => r.item === item)
      .map((r) => r.line)
    const itemWrites = writes
      .filter((w) => w.item === item)
      .map((w) => w.line)

    if (itemReads.length > 0 && itemWrites.length === 0) {
      console.log(
        `⚠️ '${item}' is READ (lines: ${itemReads.join(", ")}) but NEVER SET.`,
      )
    } else if (itemWrites.length > 0 && itemReads.length === 0) {
      console.log(
        `⚠️ '${item}' is SET (lines: ${itemWrites.join(", ")}) but NEVER READ.`,
      )
    }
  })
}

scanFile(process.argv[2])
