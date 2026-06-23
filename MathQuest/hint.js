/**
 * Hint system, reads json/hint_data.json (the output of shuffle_exits.py's
 * solver) and answers "how do I get item/room X from where I'm standing".
 *
 * Mirrors the Python solver's logic (entrance.X tokens resolve to a
 * room-qualified key, permits/skills/quests are tiered -- higher tier
 * satisfies a lower requirement, counts/tiers can be "inf"), but ALSO
 * tracks *how* each room/item was first reached so a path can be
 * reconstructed afterward, which the one-shot Python solve never needed.
 *
 * KNOWN SIMPLIFICATION: when explaining a gated step, this assumes
 * whatever item satisfies it was picked up somewhere ON the direct path
 * to the target. If the real solve required a "side trip" to a room off
 * that path, the hint will name the item but not where it came from --
 * call howGet() on that item separately to get its own path.
 */

class Hint {
  constructor(hintData) {
    this.hd = hintData
    this.graph = hintData.graph || {}
    this.locations = hintData.locations || []
    this.itemGiveIndex = hintData.itemGiveIndex || {}
    this.entranceIndex = hintData.entranceIndex || {}

    this.locationsByRoom = new Map()
    for (const loc of this.locations) {
      if (!this.locationsByRoom.has(loc.room))
        this.locationsByRoom.set(loc.room, [])
      this.locationsByRoom.get(loc.room).push(loc)
    }
  }

  // ---- token parsing (mirrors shuffle_exits.py's parse_requirement_token) ----

  static REQUIREMENT_PREFIXES = new Set([
    "entrance",
    "item",
    "skill",
    "permit",
    "quest",
    "weapon",
    "armor",
    "ring",
    "magic",
    "food",
    "drop",
    "misc",
  ])

  _parseToken(tok) {
    if ([...tok].every((c) => c === "?")) {
      return { raw: tok, type: "flag", name: tok, placeholder: true }
    }
    if (tok.startsWith("entrance.")) {
      return {
        raw: tok,
        type: "entrance",
        value: tok.slice("entrance.".length),
      }
    }
    const colonIdx = tok.indexOf(":")
    if (colonIdx !== -1) {
      const prefix = tok.slice(0, colonIdx)
      if (Hint.REQUIREMENT_PREFIXES.has(prefix)) {
        let rest = tok.slice(colonIdx + 1)
        const result = { raw: tok, type: prefix }
        const placeholder = rest.endsWith("?")
        if (placeholder) {
          rest = rest.slice(0, -1)
          result.placeholder = true
        }
        const hashIdx = rest.lastIndexOf("#")
        const dotIdx = rest.lastIndexOf(".")
        if (hashIdx !== -1) {
          result.name = rest.slice(0, hashIdx)
          const countStr = rest.slice(hashIdx + 1)
          result.count =
            /^(inf|infinite)$/i.test(countStr) ? Infinity : (
              parseIntOrNull(countStr)
            )
        } else if (dotIdx !== -1) {
          result.name = rest.slice(0, dotIdx)
          const tierStr = rest.slice(dotIdx + 1)
          result.tier =
            /^(inf|infinite)$/i.test(tierStr) ? Infinity : (
              parseIntOrNull(tierStr)
            )
        } else {
          result.name = rest
          result.count = 1
        }
        return result
      }
    }
    if (tok.includes("?")) {
      return { raw: tok, type: "flag", name: tok, placeholder: true }
    }
    return { raw: tok, type: "flag", name: tok }
  }

  _haveKey(tok, room) {
    if (tok.type === "entrance") {
      return `${fmtCoord(room[0])}.${fmtCoord(room[1])}.entrance.${tok.value}`
    }
    return `${tok.type}:${tok.name}`
  }

  _tokenSatisfied(tok, have, room) {
    if (tok.placeholder) return true
    const needed = tok.count ?? tok.tier ?? 1
    return (have.get(this._haveKey(tok, room)) || 0) >= needed
  }

  _groupSatisfied(group, have, room) {
    return group.every((t) => this._tokenSatisfied(t, have, room))
  }

  _requiresSatisfied(rawGroups, have, room) {
    if (!rawGroups || rawGroups.length === 0) return true
    return rawGroups.some((group) =>
      this._groupSatisfied(
        group.map((t) => this._parseToken(t)),
        have,
        room,
      ),
    )
  }

  // ---- solve: fixed-point reachability from a starting room, with parent
  // pointers for path reconstruction and a record of where each item/skill/
  // permit was first obtained ----

  _solve(startRoom) {
    const have = new Map()
    const cameFrom = new Map() // roomKey -> {fromRoom, edge} | null (start)
    const obtainedVia = new Map() // "type:name" -> {room, raw}
    const visited = new Set()

    const startKey = roomKeyStr(startRoom)
    visited.add(startKey)
    cameFrom.set(startKey, null)

    const tryGrantLocation = (loc) => {
      const roomTuple =
        startKey === loc.room ?
          startRoom
        : loc.room.split("_").map(Number)
      if (!this._requiresSatisfied(loc.requires, have, roomTuple))
        return false
      let grantedAny = false
      for (const raw of loc.receive || []) {
        const tok = this._parseToken(raw)
        const key = `${tok.type}:${tok.name}`
        const amount = tok.count ?? tok.tier ?? 1
        if ((have.get(key) || 0) < amount) {
          have.set(key, amount)
          grantedAny = true
        }
        if (!obtainedVia.has(key))
          obtainedVia.set(key, { room: loc.room, raw })
      }
      return grantedAny
    }

    let changed = true
    while (changed) {
      changed = false

      for (const roomKey of visited) {
        for (const loc of this.locationsByRoom.get(roomKey) || []) {
          if (tryGrantLocation(loc)) changed = true
        }
      }

      for (const roomKey of [...visited]) {
        const roomTuple = roomKey.split("_").map(Number)
        for (const edge of this.graph[roomKey] || []) {
          if (visited.has(edge.toRoom)) continue
          if (
            this._requiresSatisfied(edge.requires, have, roomTuple)
          ) {
            visited.add(edge.toRoom)
            cameFrom.set(edge.toRoom, { fromRoom: roomKey, edge })
            changed = true
          }
        }
      }
    }

    return { have, cameFrom, obtainedVia, visited }
  }

  // ---- target resolution: `thing` can be a room ({north,east} or "N_E")
  // or an item-style token/raw string ("item:key#1", "key", etc.) ----

  _resolveTarget(thing, solved) {
    if (thing && typeof thing === "object" && "north" in thing) {
      const room = roomKeyStr([thing.north, thing.east])
      return solved.visited.has(room) ? { room } : null
    }
    if (typeof thing === "string" && /^-?\d+_-?\d+$/.test(thing)) {
      return solved.visited.has(thing) ? { room: thing } : null
    }
    // item-style: try itemGiveIndex first (authoritative, matches the
    // solver's own item naming), else parse it as a token directly
    const tok = this._parseToken(String(thing))
    const key = `${tok.type}:${tok.name}`
    const obtained = solved.obtainedVia.get(key)
    if (obtained)
      return {
        room: obtained.room,
        item: tok.name,
        raw: obtained.raw,
      }
    const candidates = this.itemGiveIndex[key]
    if (candidates && candidates.length) {
      const reachable = candidates.find((c) =>
        solved.visited.has(c.room),
      )
      if (reachable)
        return {
          room: reachable.room,
          item: tok.name,
          raw: reachable.raw,
        }
    }
    return null
  }

  _reconstructRoomPath(targetRoom, cameFrom) {
    const path = []
    let cur = targetRoom
    while (cur !== undefined) {
      const prev = cameFrom.get(cur)
      path.push({ room: cur, edge: prev ? prev.edge : null })
      cur = prev ? prev.fromRoom : undefined
    }
    path.reverse()
    return path
  }

  // names, for a satisfied requires-group, which items (if any) were the
  // ones actually relied on -- used purely for the "use X to ..." text
  _namesUsedFor(rawGroups, have, room) {
    if (!rawGroups || rawGroups.length === 0) return []
    for (const group of rawGroups) {
      const parsed = group.map((t) => this._parseToken(t))
      if (this._groupSatisfied(parsed, have, room)) {
        return parsed
          .filter((t) => t.type !== "entrance" && !t.placeholder)
          .map((t) => t.name)
      }
    }
    return []
  }

  /**
   * Returns an ordered array of step objects describing how to get from
   * {px,py} to `thing` (a room or an item), or null if unreachable.
   * Step shapes:
   *   {type:"move", room, direction, gapIndex, exitId}
   *   {type:"pickup", room, item}
   *   {type:"gatedPickup", room, usedItems, item}
   *   {type:"gatedMove", room, usedItems, direction, gapIndex, exitId}
   */
  howGet(thing, { px, py } = {}) {
    const startRoom = [px, py]
    const solved = this._solve(startRoom)
    const target = this._resolveTarget(thing, solved)
    if (!target) return null

    const roomPath = this._reconstructRoomPath(
      target.room,
      solved.cameFrom,
    )
    const steps = []
    const seenLocations = new Set()

    for (const node of roomPath) {
      if (node.edge) {
        const e = node.edge
        const usedItems = this._namesUsedFor(
          e.requires,
          solved.have,
          node.room.split("_").map(Number),
        )
        if (e.requires && e.requires.length && usedItems.length) {
          steps.push({
            type: "gatedMove",
            room: node.room,
            usedItems,
            direction: e.direction,
            exitId: e.exitId,
          })
        } else {
          steps.push({
            type: "move",
            room: node.room,
            direction: e.direction,
            exitId: e.exitId,
          })
        }
      }

      for (const loc of this.locationsByRoom.get(node.room) || []) {
        const locKey = `${node.room}:${JSON.stringify(loc.receive)}`
        if (seenLocations.has(locKey)) continue
        for (const raw of loc.receive || []) {
          const tok = this._parseToken(raw)
          const key = `${tok.type}:${tok.name}`
          const via = solved.obtainedVia.get(key)
          if (!via || via.room !== node.room) continue
          seenLocations.add(locKey)
          if (loc.requires && loc.requires.length) {
            const used = this._namesUsedFor(
              loc.requires,
              solved.have,
              node.room.split("_").map(Number),
            )
            steps.push({
              type: "gatedPickup",
              room: node.room,
              usedItems: used,
              item: tok.name,
            })
          } else {
            steps.push({
              type: "pickup",
              room: node.room,
              item: tok.name,
            })
          }
        }
      }
    }

    return steps
  }

  /**
   * Same as howGet, but returns (and logs) a human-readable multi-line
   * string, e.g.:
   *   20_20 exit south0
   *   get item gold
   *   14_25 use bomb to get key
   */
  showFullPath(thing, pos = {}) {
    const steps = this.howGet(thing, pos)
    if (!steps) {
      const msg = `no known path to ${JSON.stringify(thing)} from ${JSON.stringify(pos)}`
      console.log(msg)
      return msg
    }
    const lines = steps.map((s) => {
      switch (s.type) {
        case "move":
          return `${s.room} exit ${s.direction}${s.exitGapLabel ?? ""}`
        case "gatedMove":
          return `${s.room} use ${s.usedItems.join(" + ")} to exit ${s.direction}`
        case "pickup":
          return `get item ${s.item}`
        case "gatedPickup":
          return `${s.room} use ${s.usedItems.join(" + ")} to get ${s.item}`
        default:
          return `(unknown step ${JSON.stringify(s)})`
      }
    })
    const text = lines.join("\n")
    console.log(text)
    return text
  }
}

function fmtCoord(n) {
  return Number.isInteger(n) ? String(n) : String(n)
}

function roomKeyStr([n, e]) {
  return `${fmtCoord(n)}_${fmtCoord(e)}`
}

function parseIntOrNull(s) {
  const n = parseInt(s, 10)
  return Number.isNaN(n) ? null : n
}

// --- usage ---
// Node:
//   const fs = require("fs")
//   const hd = JSON.parse(fs.readFileSync("./json/hint_data.json", "utf8"))
//   const hint = new Hint(hd)
//   hint.showFullPath("item:key", { px: 20, py: 20 })
//
// Browser:
//   const hd = await fetch("./json/hint_data.json").then(r => r.json())
//   const hint = new Hint(hd)
//   hint.showFullPath("item:key", { px: 20, py: 20 })

if (typeof module !== "undefined" && module.exports) {
  module.exports = { Hint }
}
