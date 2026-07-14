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
  let warpIndex = null // "room|side|idx" -> [{ reqs, targets: [{room,side,idx}] }]

  function buildRoomIndex() {
    roomIndex = {}
    for (const r of ap.slotData.AP_ENTRANCE_IDS) {
      roomIndex[`${r.north}_${r.east}`] = r
    }
  }

  // Indexes _room_geometry.WARPS (emitted as WARPS_DATA by gen_map.py) by
  // origin exit so the BFS below can fire them off the moment that exit
  // becomes reachable, same as it does for physical doorways.
  //
  // Matches regions.py's _connect_warps_vanilla exactly: every connection in
  // a warp group -- root ones included -- gets a fully bidirectional edge
  // to/from the shared warp hub. Root is *reachable* like any other node
  // (see markExitReachable's automatic exit->root feed below) and, once
  // reached, is just as valid a warp origin as a real exit.
  function buildWarpIndex() {
    warpIndex = {}
    const warps = (typeof WARPS_DATA !== "undefined" && WARPS_DATA) || []
    for (const warp of warps) {
      const reqs = warp.reqs || []
      const conns = warp.connections || []
      conns.forEach(([n, e, side, idx], oi) => {
        const originKey = `${n}_${e}|${side}|${idx}`
        const targets = conns
          .filter((_, di) => di !== oi)
          .map(([tn, te, tside, tidx]) => ({
            room: `${tn}_${te}`,
            side: tside,
            idx: tidx,
          }))
        if (!warpIndex[originKey]) warpIndex[originKey] = []
        warpIndex[originKey].push({ reqs, targets })
      })
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
    if (!warpIndex) buildWarpIndex()
    QuestState.seedFromGame()

    const reachableExits = new Set()
    const roomExitCounts = {}
    const visitedRooms = new Set()
    const queue = []

    function totalExitsFor(room) {
      let n = 0
      for (const side of Object.keys(room.exits || {}))
        n += room.exits[side].length
      return n
    }

    function ensureCounts(roomKey, room) {
      if (!roomExitCounts[roomKey]) {
        roomExitCounts[roomKey] = {
          reachable: 0,
          total: totalExitsFor(room),
        }
      }
    }

    // Marks one exit (or the room's single "root" node) reachable, if it
    // isn't already, and queues it for further expansion. Every node that
    // becomes reachable this way also gets a chance to fire off any warp
    // whose origin is that exact node.
    //
    // Matches regions.py's Pass 1 exactly: every real exit gets a one-way,
    // unconditional edge straight into its room's root (so root becomes
    // reachable the moment ANY exit of the room is), but root has no edge
    // back out to any of the room's real exits -- the only way out of root
    // is another warp anchored there. So root only ever gets *fed*, it
    // never triggers the area-component expansion real exits do.
    function markExitReachable(roomKey, side, idx) {
      const node = `${roomKey}|${side}|${idx}`
      if (reachableExits.has(node)) return
      const room = roomIndex[roomKey]
      if (!room) return
      ensureCounts(roomKey, room)
      reachableExits.add(node)
      if (side !== "root") {
        roomExitCounts[roomKey].reachable++
        markExitReachable(roomKey, "root", 0)
      }
      queue.push({ room: roomKey, side, idx })
    }

    // "Seeds" a room the way actually starting there works: every exit
    // becomes reachable at once, regardless of area/reqs gating between
    // them, since the player is simply standing inside the room rather
    // than having walked in through one specific gated exit. Used only for
    // the real starting room (see the `startRoom` seed below) -- NOT for
    // warps landing at a room's root, which per regions.py do NOT grant
    // access to that room's other exits (see markExitReachable above).
    function seedRoomFully(roomKey) {
      const room = roomIndex[roomKey]
      if (!room) return
      visitedRooms.add(roomKey)
      ensureCounts(roomKey, room)
      // Seed root directly too: a room that's purely a warp hub (no
      // physical doors at all) would otherwise never feed its root, since
      // that normally only happens via a real exit's exit->root edge --
      // and there are no exits here to provide one.
      markExitReachable(roomKey, "root", 0)
      const comps = computeRoomComponents(room, haveReal)
      for (const key of Object.keys(comps)) {
        const side = key.replace(/\d+$/, "")
        const idx = Number(key.match(/\d+$/)[0])
        markExitReachable(roomKey, side, idx)
      }
    }

    // Arriving through one specific real exit of a room (a physical
    // doorway, or a warp landing at a non-root connection): that exit
    // becomes reachable, and so does the rest of its area-component
    // (whatever's walkable from there given the room's current reqs-gated
    // internal connectivity).
    function enterRoomViaExit(roomKey, side, idx) {
      const room = roomIndex[roomKey]
      if (!room) return
      visitedRooms.add(roomKey)
      markExitReachable(roomKey, side, idx)
      const comps = computeRoomComponents(room, haveReal)
      const enteredComp = comps[exitKey(side, idx)]
      if (enteredComp === undefined) return
      for (const key of Object.keys(comps)) {
        if (comps[key] !== enteredComp) continue
        const s = key.replace(/\d+$/, "")
        const i = Number(key.match(/\d+$/)[0])
        markExitReachable(roomKey, s, i)
      }
    }

    // Fires any WARPS group whose origin is this exact node (a real exit,
    // or a room's root once fed), once its reqs are satisfied. A "root"
    // target is just marked reachable (matching regions.py: warp -> root
    // grants nothing beyond root itself); any other target is entered
    // exactly like a physical doorway would be.
    function fireWarpsFrom(roomKey, side, idx) {
      const entries = warpIndex[`${roomKey}|${side}|${idx}`]
      if (!entries) return
      for (const { reqs, targets } of entries) {
        if (!reqsSatisfied(reqs, haveReal)) continue
        for (const t of targets) {
          if (t.side === "root") markExitReachable(t.room, "root", 0)
          else enterRoomViaExit(t.room, t.side, t.idx)
        }
      }
    }

    if (roomIndex[startRoom]) seedRoomFully(startRoom)

    while (queue.length > 0) {
      const cur = queue.shift()
      const room = roomIndex[cur.room]
      if (!room) continue

      fireWarpsFrom(cur.room, cur.side, cur.idx)

      // Root has no physical doorway of its own to cross through.
      if (cur.side === "root") continue

      const dest = externalConnection(
        cur.room,
        room,
        cur.side,
        cur.idx,
      )
      if (dest && roomIndex[dest.room]) {
        enterRoomViaExit(dest.room, dest.side, dest.idx)
      }
    }

    function isEntranceReachable(room, side, idx) {
      return reachableExits.has(`${room}|${side}|${idx}`)
    }

    function roomStatus(room) {
      const counts = roomExitCounts[room]
      if (!roomIndex[room]) return "full" // no entrance data at all: don't grey, unknown
      if (!counts || counts.total === 0)
        return visitedRooms.has(room) ? "full" : "full"
      if (counts.reachable === 0) return "full"
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
