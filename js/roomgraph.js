// Physical map traversal / room reachability engine.
// Builds a graph of room exits, applies entrance-rando overrides (ER_MAP) or
// vanilla adjacency, and BFSes from the start room (20,20) given the current
// real-item "have" set. Feeds room-level grey-out classes AND resolves
// entrance.* tokens for logic.js (replacing the old always-"unknown" stub).

const RoomGraph = (function () {
  const DIRS = {
    north: { dn: 1, de: 0, opposite: "south" },
    south: { dn: -1, de: 0, opposite: "north" },
    east: { dn: 0, de: 1, opposite: "west" },
    west: { dn: 0, de: -1, opposite: "east" },
  }

  let roomIndex = null // "north_east" -> room entry from AP_ENTRANCE_IDS

  function buildRoomIndex() {
    roomIndex = {}
    for (const r of ap.slotData.AP_ENTRANCE_IDS) {
      roomIndex[`${r.north}_${r.east}`] = r
    }
  }

  // Same 3-state evaluator as logic.js, but simplified: room-internal reqs
  // aren't expected to reference entrance.* tokens, so any that do are
  // treated as an automatic pass (optimistic) rather than stalling the graph.
  function reqsSatisfied(reqGroups, have) {
    if (!reqGroups || reqGroups.length === 0) return true
    return reqGroups.some((group) =>
      group.every((rawTok) => {
        const tok = rawTok.split("#")[0]
        if (tok.startsWith("entrance.")) return true
        if (tok.startsWith("quest:")) return QuestState.satisfied(tok)
        return have.has(tok)
      }),
    )
  }

  function exitKey(side, idx) {
    return `${side}${idx}`
  }

  // Union-find over this room's own exits, given which "areas" entries are
  // currently satisfied. Returns Map<"side idx", componentId(int)>.
  function computeRoomComponents(room, have) {
    const parent = {}
    function find(x) {
      while (parent[x] !== x) {
        parent[x] = parent[parent[x]]
        x = parent[x]
      }
      return x
    }
    function union(a, b) {
      const ra = find(a),
        rb = find(b)
      if (ra !== rb) parent[ra] = rb
    }

    const allKeys = []
    for (const side of Object.keys(room.exits || {})) {
      room.exits[side].forEach((_, idx) => {
        const k = exitKey(side, idx)
        parent[k] = k
        allKeys.push(k)
      })
    }

    if (!room.areas || room.areas.length === 0) {
      // no partitioning data at all: every exit is mutually reachable
      for (let i = 1; i < allKeys.length; i++)
        union(allKeys[0], allKeys[i])
    } else {
      for (const entry of room.areas) {
        if (!reqsSatisfied(entry.reqs, have)) continue
        for (const group of entry.areas) {
          for (let i = 1; i < group.length; i++) {
            const a = exitKey(group[0].side, group[0].idx)
            const b = exitKey(group[i].side, group[i].idx)
            if (parent[a] === undefined || parent[b] === undefined)
              continue
            union(a, b)
          }
        }
      }
    }

    const comp = {}
    for (const k of Object.keys(parent)) comp[k] = find(k)
    return comp
  }

  // Resolve the external connection for a given room exit: ER_MAP override
  // if it exists and matches, otherwise vanilla same-idx opposite-side neighbor.
  function externalConnection(roomKey, room, side, idx) {
    const [north, east] = roomKey.split("_").map(Number)
    const d = DIRS[side]

    const conns = (ER_MAP.get(roomKey) || []).filter(
      (c) => c.origSide === side,
    )
    if (conns.length > 0) {
      const exact = conns.find(
        (c) => String(c.origIdx) === String(idx),
      )
      const conn = exact || conns[0]
      return {
        room: `${conn.newNorth}_${conn.newEast}`,
        side: conn.exitSide,
        idx: Number(conn.exitIdx),
      }
    }

    // vanilla fallback: same idx, opposite side, grid neighbor
    const vanillaNorth = north + d.dn
    const vanillaEast = east + d.de
    const neighborKey = `${vanillaNorth}_${vanillaEast}`
    if (!roomIndex[neighborKey]) return null // no room there at all
    return { room: neighborKey, side: d.opposite, idx }
  }

  // Full BFS given a Set of real items currently "have". Returns:
  //   reachableExits: Set of "room|side|idx"
  //   roomExitCounts: Map<room, {reachable, total}>
  //   isEntranceReachable(room, side, idx): bool
  function computeReachability(haveReal, startRoom) {
    if (!roomIndex) buildRoomIndex()
    QuestState.seedFromGame()

    const reachableExits = new Set()
    const roomExitCounts = {}

    function totalExitsFor(room) {
      let n = 0
      for (const side of Object.keys(room.exits || {}))
        n += room.exits[side].length
      return n
    }

    const queue = []
    const visitedRooms = new Set()

    // Seed: start room, union ALL satisfied components (not gated by entry side,
    // since the player begins inside it rather than walking in from an exit).
    if (roomIndex[startRoom]) {
      const room = roomIndex[startRoom]
      const total = totalExitsFor(room)
      roomExitCounts[startRoom] = { reachable: 0, total }
      const comps = computeRoomComponents(room, haveReal)
      for (const key of Object.keys(comps)) {
        const [side, idxStr] = [
          key.replace(/\d+$/, ""),
          key.match(/\d+$/)[0],
        ]
        const idx = Number(idxStr)
        const node = `${startRoom}|${side}|${idx}`
        if (!reachableExits.has(node)) {
          reachableExits.add(node)
          roomExitCounts[startRoom].reachable++
          queue.push({ room: startRoom, side, idx })
        }
      }
      visitedRooms.add(startRoom)
    }

    while (queue.length > 0) {
      const cur = queue.shift()
      const room = roomIndex[cur.room]
      if (!room) continue

      // step 1: cross to the neighboring room's connecting exit
      const dest = externalConnection(
        cur.room,
        room,
        cur.side,
        cur.idx,
      )
      if (dest && roomIndex[dest.room]) {
        const destRoom = roomIndex[dest.room]
        if (!roomExitCounts[dest.room]) {
          roomExitCounts[dest.room] = {
            reachable: 0,
            total: totalExitsFor(destRoom),
          }
        }
        const destNode = `${dest.room}|${dest.side}|${dest.idx}`
        if (!reachableExits.has(destNode)) {
          reachableExits.add(destNode)
          roomExitCounts[dest.room].reachable++
          queue.push({
            room: dest.room,
            side: dest.side,
            idx: dest.idx,
          })
        }

        // step 2: from that entry exit, expand to the rest of ITS room's
        // same-component exits (only reachable via this specific entry side)
        const comps = computeRoomComponents(destRoom, haveReal)
        const enteredKey = exitKey(dest.side, dest.idx)
        const enteredComp = comps[enteredKey]
        if (enteredComp !== undefined) {
          for (const key of Object.keys(comps)) {
            if (comps[key] !== enteredComp) continue
            const side = key.replace(/\d+$/, "")
            const idx = Number(key.match(/\d+$/)[0])
            const node = `${dest.room}|${side}|${idx}`
            if (!reachableExits.has(node)) {
              reachableExits.add(node)
              roomExitCounts[dest.room].reachable++
              queue.push({ room: dest.room, side, idx })
            }
          }
        }
        visitedRooms.add(dest.room)
      }
    }

    function isEntranceReachable(room, side, idx) {
      return reachableExits.has(`${room}|${side}|${idx}`)
    }

    function roomStatus(room) {
      const counts = roomExitCounts[room]
      if (!roomIndex[room]) return "full" // no entrance data at all: don't grey, unknown
      if (!counts || counts.total === 0)
        return visitedRooms.has(room) ? "full" : "none"
      if (counts.reachable === 0) return "none"
      if (counts.reachable >= counts.total) return "full"
      return "partial"
    }

    return {
      reachableExits,
      roomExitCounts,
      isEntranceReachable,
      roomStatus,
      visitedRooms,
    }
  }

  return { computeReachability }
})()
