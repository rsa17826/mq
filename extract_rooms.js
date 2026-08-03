// extract_rooms.js
//
// Walks MathQuest.js looking for the room-setup blocks of the form:
//   if (manager.north == N && manager.east == E) { ... }
// and pulls out:
//   - ground / area
//   - the scene collision string
//   - every manager.<obj>[idx?].set_x/set_y/set_visible/set_text(...) call,
//     annotated with the full chain of guard conditions (nested ifs) that
//     have to be true for that statement to run.
//
// Usage: node extract_rooms.js MathQuest.js > rooms.json

const acorn = require("acorn")
const fs = require("fs")

const SRC_PATH = process.argv[2]
if (!SRC_PATH) {
  console.error("usage: node extract_rooms.js <path-to-MathQuest.js>")
  process.exit(1)
}
const src = fs.readFileSync(SRC_PATH, "utf8")
const ast = acorn.parse(src, { ecmaVersion: 2022, sourceType: "script" })

function srcOf(node) {
  return src.slice(node.start, node.end)
}

// Is this `manager.north == <num>` or `<num> == manager.north` etc, for
// either north or east? Returns { field: 'north'|'east', value } or null.
function matchNorthEastCompare(node) {
  if (node.type !== "BinaryExpression" || node.operator !== "==") return null
  const sides = [node.left, node.right]
  for (const side of sides) {
    if (
      side.type === "MemberExpression" &&
      side.object.type === "Identifier" &&
      side.object.name === "manager" &&
      side.property.type === "Identifier" &&
      (side.property.name === "north" || side.property.name === "east")
    ) {
      const other = side === node.left ? node.right : node.left
      if (other.type === "Literal" && typeof other.value === "number") {
        return { field: side.property.name, value: other.value }
      }
    }
  }
  return null
}

// Is `test` a `manager.north == N && manager.east == E` (either order,
// possibly with extra parens)? Returns {north, east} or null.
function matchRoomGuard(test) {
  if (test.type !== "LogicalExpression" || test.operator !== "&&") return null
  const a = matchNorthEastCompare(test.left)
  const b = matchNorthEastCompare(test.right)
  if (!a || !b) return null
  if (a.field === b.field) return null
  const out = {}
  out[a.field] = a.value
  out[b.field] = b.value
  return out
}

// Turn `manager.foo` / `manager.foo[3]` / `manager.foo[i]` into a stable
// string path, and separately a { base, index } pair.
function memberPath(node) {
  if (node.type === "MemberExpression") {
    if (!node.computed) {
      return memberPath(node.object) + "." + node.property.name
    } else {
      return memberPath(node.object) + "[" + srcOf(node.property) + "]"
    }
  }
  if (node.type === "Identifier") return node.name
  return srcOf(node)
}

function isManagerCall(node, methodNames) {
  return (
    node.type === "CallExpression" &&
    node.callee.type === "MemberExpression" &&
    !node.callee.computed &&
    methodNames.includes(node.callee.property.name) &&
    srcOf(node.callee.object).startsWith("manager.")
  )
}

const SETTERS = ["set_x", "set_y", "set_visible", "set_text"]

function extractRoomBody(bodyNode, guardStack, objects) {
  const stmts = bodyNode.type === "BlockStatement" ? bodyNode.body : [bodyNode]
  for (const stmt of stmts) {
    if (stmt.type === "IfStatement") {
      // Skip the improbable case of an inner north/east recheck; treat
      // every nested if as an additional guard condition.
      const guard = srcOf(stmt.test)
      extractRoomBody(stmt.consequent, [...guardStack, guard], objects)
      if (stmt.alternate) {
        extractRoomBody(stmt.alternate, [...guardStack, `!(${guard})`], objects)
      }
      continue
    }
    if (stmt.type === "ExpressionStatement") {
      const expr = stmt.expression
      if (isManagerCall(expr, SETTERS)) {
        const target = memberPath(expr.callee.object)
        const method = expr.callee.property.name
        const arg = expr.arguments[0] ? srcOf(expr.arguments[0]) : null
        objects.push({
          target,
          method,
          arg,
          guard: guardStack.length ? guardStack.join(" && ") : null,
        })
      }
      continue
    }
    // Other statement types inside a room block (assignments to
    // manager.ground/.area/__createObject.scene, loops, etc) are walked
    // shallowly for nested ifs only; extend here if you find useful data
    // inside for/while blocks.
    if (stmt.type === "BlockStatement") {
      extractRoomBody(stmt, guardStack, objects)
    }
  }
}

function findSceneAssignment(bodyNode) {
  const stmts = bodyNode.body
  for (const stmt of stmts) {
    if (
      stmt.type === "ExpressionStatement" &&
      stmt.expression.type === "AssignmentExpression" &&
      srcOf(stmt.expression.left) === "__createObject.scene"
    ) {
      // RHS is "....".split("") -- pull the string literal out.
      const rhs = stmt.expression.right
      if (
        rhs.type === "CallExpression" &&
        rhs.callee.type === "MemberExpression" &&
        rhs.callee.property.name === "split" &&
        rhs.callee.object.type === "Literal"
      ) {
        return rhs.callee.object.value
      }
    }
  }
  return null
}

function findSimpleAssignment(bodyNode, propName) {
  for (const stmt of bodyNode.body) {
    if (
      stmt.type === "ExpressionStatement" &&
      stmt.expression.type === "AssignmentExpression" &&
      stmt.expression.left.type === "MemberExpression" &&
      srcOf(stmt.expression.left.object) === "manager" &&
      stmt.expression.left.property.name === propName
    ) {
      const rhs = stmt.expression.right
      return rhs.type === "Literal" ? rhs.value : srcOf(rhs)
    }
  }
  return null
}

// roomKey -> room record. The same `if (manager.north == N && manager.east
// == E)` guard shape shows up all over the file for dialogue handlers, shop
// logic, teleport nudges, etc -- not just the one canonical scene-setup
// block per room. We only treat a match as "the room" if it actually
// assigns __createObject.scene (or at minimum manager.ground) in that
// block; every other coincidental match is skipped rather than producing a
// near-empty duplicate entry.
const roomsByKey = new Map()
const skippedNonSceneMatches = []

function walk(node) {
  if (!node || typeof node.type !== "string") return
  if (node.type === "IfStatement") {
    const roomGuard = matchRoomGuard(node.test)
    if (roomGuard && node.consequent.type === "BlockStatement") {
      const ground = findSimpleAssignment(node.consequent, "ground")
      const area = findSimpleAssignment(node.consequent, "area")
      const scene = findSceneAssignment(node.consequent)
      const key = `${roomGuard.north}_${roomGuard.east}`

      if (scene === null && ground === null) {
        // Not the scene-setup block for this room -- some other bit of
        // logic (dialogue, shop, teleport-adjust, etc) that happens to
        // gate on the same coordinates. Record it in case it's useful
        // later (e.g. conditional shop objects like tradeButton) but
        // don't let it clobber/duplicate the real room entry.
        skippedNonSceneMatches.push({
          north: roomGuard.north,
          east: roomGuard.east,
          snippet: srcOf(node.consequent).slice(0, 200),
        })
      } else {
        const objects = []
        extractRoomBody(node.consequent, [], objects)
        if (roomsByKey.has(key)) {
          // Legitimately more than one scene-setup-shaped block for this
          // room (hasn't been observed, but merge defensively rather than
          // silently dropping data).
          const existing = roomsByKey.get(key)
          existing.ground = existing.ground ?? ground
          existing.area = existing.area ?? area
          existing.scene = existing.scene ?? scene
          existing.objects.push(...objects)
        } else {
          roomsByKey.set(key, {
            north: roomGuard.north,
            east: roomGuard.east,
            ground,
            area,
            scene,
            objects,
          })
        }
      }
    }
  }
  for (const key in node) {
    if (key === "start" || key === "end" || key === "loc" || key === "range") continue
    const val = node[key]
    if (Array.isArray(val)) {
      for (const child of val) walk(child)
    } else if (val && typeof val.type === "string") {
      walk(val)
    }
  }
}

walk(ast)

const rooms = [...roomsByKey.values()]

if (process.env.DEBUG_SKIPPED) {
  fs.writeFileSync(
    "skipped_matches.json",
    JSON.stringify(skippedNonSceneMatches, null, 2),
  )
  console.error(
    `wrote ${skippedNonSceneMatches.length} skipped non-scene matches to skipped_matches.json`,
  )
}

process.stdout.write(JSON.stringify(rooms, null, 2))
