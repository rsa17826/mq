// Reachability / logic engine.
// Requires PROG_DATA (prog.js), ap.slotData.AP_ITEM_IDS (game globals), and tracker.js's
// data-location markers to already be present on the page.

;(function () {
  function init() {
    if (!window.ap?.slotData?.AP_LOCATION_IDS) {
      setTimeout(init, 250)
      return
    }

    // Ground truth for "is this token a real network item" (vs a free/virtual
    // flag like area:/quest:, or an unresolvable entrance.* token).
    const REAL_ITEM_NAMES = new Set(Object.values(ap.slotData.AP_ITEM_IDS))

    function isEntranceToken(tok) {
      return tok.startsWith("entrance.")
    }

    function parseEntranceToken(tok) {
      const m = tok.match(/^entrance\.(north|south|east|west)(\d+)$/)
      if (!m) return null
      return { side: m[1], idx: Number(m[2]) }
    }

    // Cache icon elements by their "room - item" location key.
    const iconsByLocation = {}
    document
      .querySelectorAll(".progression-icon[data-location]")
      .forEach((el) => {
        // ANCHOR exclude some icons from prog checks
        if (["area:", "flag:"].find((e) => el.alt.startsWith(e))) {
          return
        }
        ;(iconsByLocation[el.dataset.location] ||= []).push(el)
      })

    const roomEls = {}
    document
      .querySelectorAll(".tile-wrapper[data-room]")
      .forEach((el) => {
        roomEls[el.dataset.room] = el
      })

    const haveReal = new Set() // real items actually received over the network
    window.haveReal = haveReal
    // NOTE temp
    haveReal.add("item:gold")

    function baseTok(tok) {
      return tok.split("#")[0]
    }

    // Evaluate one AND-group given a room context (for resolving entrance.*
    // tokens against the room graph). Returns 'true' / 'false' / 'unknown'
    // ('unknown' only happens if we have no entrance data for that room at all).
    function evalGroup(group, have, roomKey, roomGraph) {
      if (group.length === 0) return "true"
      for (const rawTok of group) {
        const tok = baseTok(rawTok)
        if (isEntranceToken(tok)) {
          const parsed = parseEntranceToken(tok)
          if (!parsed || !roomGraph) return "unknown"
          if (!roomGraph.reachableExits) return "unknown"
          const known =
            roomGraph.roomExitCounts[roomKey] !== undefined ||
            roomGraph.isEntranceReachable(
              roomKey,
              parsed.side,
              parsed.idx,
            )
          if (!known) return "unknown"
          if (
            !roomGraph.isEntranceReachable(
              roomKey,
              parsed.side,
              parsed.idx,
            )
          )
            return "false"
          continue
        }
        if (tok.startsWith("quest:")) {
          if (!QuestState.satisfied(tok)) return "false"
          continue
        }
        if (!have.has(tok)) return "false"
      }
      return "true"
    }

    // Evaluate an entry: best result across its OR-groups. An entry can only
    // ever resolve true if its own room is physically reachable at all --
    // otherwise "requires: [[]]" would trivially grant its receive tokens
    // regardless of whether the player can ever stand in that room.
    function evalEntry(entry, have, roomGraph) {
      if (roomGraph && roomGraph.roomStatus(entry.room) === "none") {
        return "false"
      }
      let best = "false"
      for (const group of entry.requires || []) {
        const r = evalGroup(group, have, entry.room, roomGraph)
        if (r === "true") return "true"
        if (r === "unknown") best = "unknown"
      }
      return best
    }

    function recompute() {
      QuestState.seedFromGame()
      const have = new Set(haveReal)
      const roomGraph = RoomGraph.computeReachability(
        haveReal,
        "20_20",
      )

      const status = new Array(PROG_DATA.length).fill("false")
      let changed = true

      while (changed) {
        changed = false
        for (let i = 0; i < PROG_DATA.length; i++) {
          if (status[i] === "true") continue // already fully resolved
          const entry = PROG_DATA[i]
          const r = evalEntry(entry, have, roomGraph)
          status[i] = r
          if (r === "true") {
            for (const rawTok of entry.receive) {
              const tok = baseTok(rawTok)
              // only virtual/free tokens auto-propagate; real items only
              // enter `have` via actual ReceivedItems packets
              if (!REAL_ITEM_NAMES.has(tok) && !have.has(tok)) {
                have.add(tok)
                changed = true
              }
            }
          }
        }
      }

      // Clear old logic markers, but never touch .checked (that's ground truth)
      document
        .querySelectorAll(
          ".progression-icon.in-logic, .progression-icon.route-unknown, .progression-icon.out-of-logic",
        )
        .forEach((el) =>
          el.classList.remove(
            "in-logic",
            "route-unknown",
            "out-of-logic",
          ),
        )

      const roomsWithAvailableItems = new Set()
      const roomsWithAvailableQuests = new Set()

      PROG_DATA.forEach((entry, i) => {
        const r = status[i]
        for (const rawTok of entry.receive) {
          const tok = baseTok(rawTok)
          const key = `${entry.room} - ${tok}`
          const els = iconsByLocation[key]
          if (!els) continue
          const isQuest = tok.startsWith("quest:")
          const questDone = isQuest && QuestState.satisfied(tok)
          const alreadyChecked =
            els.some((el) => el.classList.contains("checked")) ||
            questDone

          if (r === "true" && !alreadyChecked) {
            if (REAL_ITEM_NAMES.has(tok))
              roomsWithAvailableItems.add(entry.room)
            if (isQuest) roomsWithAvailableQuests.add(entry.room)
          }

          els.forEach((el) => {
            if (el.classList.contains("checked")) return // already collected, leave alone
            if (questDone) {
              el.classList.add("checked")
              return
            }
            if (r === "true") el.classList.add("in-logic")
            else if (r === "unknown")
              el.classList.add("route-unknown")
            else el.classList.add("out-of-logic")
          })
        }
      })

      for (const roomKey of Object.keys(roomEls)) {
        roomEls[roomKey].classList.toggle(
          "room-has-available-item",
          roomsWithAvailableItems.has(roomKey),
        )
        roomEls[roomKey].classList.toggle(
          "room-has-available-quest",
          roomsWithAvailableQuests.has(roomKey) &&
            !roomsWithAvailableItems.has(roomKey),
        )
      }

      // Room-level grey overlay based on physical reachability
      if (roomGraph) {
        for (const roomKey of Object.keys(roomEls)) {
          const el = roomEls[roomKey]
          el.classList.remove("room-unreachable", "room-partial")
          const st = roomGraph.roomStatus(roomKey)
          if (st === "none") el.classList.add("room-unreachable")
          else if (st === "partial") el.classList.add("room-partial")
        }
      }
    }

    const origOnReceivedItems = ap.onReceivedItems.bind(ap)
    ap.onReceivedItems = function (packet) {
      origOnReceivedItems(packet)
      if (!window.playerLoaded) return
      packet.items.forEach((item) => {
        const name = ap.slotData.AP_ITEM_IDS[item.item]
        if (name) haveReal.add(name)
      })
      recompute()
    }

    const origOnConnected = ap.onConnected.bind(ap)
    ap.onConnected = function (packet) {
      origOnConnected(packet)
      recompute()
    }

    recompute()
    window.__trackerRecompute = recompute
    console.log(
      `[logic] reachability engine ready: ${PROG_DATA.length} entries`,
    )
  }

  init()
})()
