const acorn = require("acorn")
const fs = require("fs")
const code = fs.readFileSync("MathQuest/MathQuest.js", "utf8")
const ast = acorn.parse(code, { ecmaVersion: "latest" })
let count = 0

function isDeclPosition(node, parent) {
  if (!parent) return false
  if (parent.type === "VariableDeclarator" && parent.id === node)
    return true
  if (
    (parent.type === "FunctionDeclaration" ||
      parent.type === "FunctionExpression") &&
    parent.id === node
  )
    return true
  if (Array.isArray(parent.params) && parent.params.includes(node))
    return true
  if (parent.type === "CatchClause" && parent.param === node)
    return true
  return false
}

function walk(node, parent) {
  if (!node || typeof node !== "object") return
  if (node.type === "Identifier" && isDeclPosition(node, parent))
    count++
  for (const key in node) {
    const val = node[key]
    if (Array.isArray(val)) val.forEach((v) => walk(v, node))
    else if (val && val.type) walk(val, node)
  }
}
walk(ast, null)
console.log("Total declaration sites:", count)
