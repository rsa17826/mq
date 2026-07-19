// Reachability / logic engine.
// Requires PROG_DATA (prog.js), ap.slotData.AP_ITEM_IDS (game globals), and tracker.js's
// data-location markers to already be present on the page.

class Logic {
  static pwcount = 0
  static pacount = 0
  static pmcount = 0
  // Ground truth for "is this token a real network item" (vs a free/virtual
  // flag like area:/quest:, or an unresolvable entrance.* token).
  /**@type {Set<string>} */
  static REAL_ITEM_NAMES = new Set()

  /**
   *
   * @param {string} tok
   * @returns
   */
  static isEntranceToken(tok) {
    return tok.startsWith("entrance.")
  }

  static parseEntranceToken(tok) {
    const m = tok.match(/^entrance\.(north|south|east|west)(\d+)$/)
    if (!m) return null
    return { side: m[1], idx: Number(m[2]) }
  }

  // Cache icon elements by their "room - item" location key.
  static iconsByLocation = {}

  static roomEls = {}

  /**@type {Set<string>} */
  static haveReal = new Set() // real items actually received over the network

  /**
   *
   * @param {string} tok
   * @returns
   */
  static baseTok(tok) {
    return tok.split("#")[0]
  }

  // Evaluate one AND-group given a room context (for resolving entrance.*
  // tokens against the room graph). Returns 'true' / 'false' / 'unknown'
  // ('unknown' only happens if we have no entrance data for that room at all).
  /**
   *
   * @param {string[]} group
   * @param {Set<string>} have
   * @param {string} roomKey
   * @param {RoomGraphReachability} roomGraph
   * @returns
   */
  static evalGroup(group, have, roomKey, roomGraph) {
    if (group.length === 0) return "true"
    for (const rawTok of group) {
      const tok = Logic.baseTok(rawTok)
      if (Logic.isEntranceToken(tok)) {
        const parsed = Logic.parseEntranceToken(tok)
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
  /**
   *
   * @param {Entry} entry
   * @param {string} have
   * @param {RoomGraphReachability} roomGraph
   * @returns
   */
  static evalEntry(entry, have, roomGraph) {
    if (roomGraph && roomGraph.roomStatus(entry.room) === "none") {
      return "false"
    }
    let best = "false"
    for (const group of entry.requires || []) {
      const r = Logic.evalGroup(group, have, entry.room, roomGraph)
      if (r === "true") return "true"
      if (r === "unknown") best = "unknown"
    }
    return best
  }

  static recompute() {
    QuestState.seedFromGame()
    const have = new Set(haveReal)
    // Room-internal `areas` gating can depend on virtual tokens (like
    // "flag:...") that only exist once some PROG_DATA entry grants them
    // below -- so `roomGraph` has to be rebuilt with the growing `have`
    // set as those get derived, not just seeded once from haveReal.
    let roomGraph = RoomGraph.computeReachability(have, "20_20")

    const status = new Array(PROG_DATA.length).fill("false")
    let changed = true

    while (changed) {
      changed = false
      for (let i = 0; i < PROG_DATA.length; i++) {
        if (status[i] === "true") continue // already fully resolved
        const entry = PROG_DATA[i]
        const r = Logic.evalEntry(entry, have, roomGraph)
        status[i] = r
        if (r === "true") {
          for (const rawTok of entry.receive) {
            const tok = Logic.baseTok(rawTok)
            // only virtual/free tokens auto-propagate; real items only
            // enter `have` via actual ReceivedItems packets
            if (!REAL_ITEM_NAMES.has(tok) && !have.has(tok)) {
              have.add(tok)
              changed = true
            }
          }
        }
      }
      if (changed) {
        // A newly derived flag/quest token might satisfy an `areas` reqs
        // group somewhere, opening a new room-internal connection (and
        // thus reachability for some entrance.* token) -- recompute the
        // physical graph before the next pass over PROG_DATA sees it.
        roomGraph = RoomGraph.computeReachability(have, "20_20")
      }
    }
    // Expose the fully-derived set (real items + every virtual/free token
    // unlocked above) so map.js's own pathfinding graph sees exactly the
    // same flags/quests this reachability pass did, instead of just the
    // raw network items -- otherwise a warp/area gated behind a purely
    // logical flag (never a real item) could never resolve to a walkable
    // path there, only a "no route" direct-pointer arrow.
    window.haveDerived = have

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
        const tok = Logic.baseTok(rawTok)
        const key = `${entry.room} - ${tok}`
        const els = Logic.iconsByLocation[key]
        if (!els) continue
        const isQuest = tok.startsWith("quest:")
        const questDone = isQuest && QuestState.satisfied(tok)
        const alreadyChecked =
          els.some((el) => el.classList.contains("checked")) ||
          questDone

        if (r === "true" && !alreadyChecked) {
          if (Logic.REAL_ITEM_NAMES.has(tok))
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
          else if (r === "unknown") el.classList.add("route-unknown")
          else el.classList.add("out-of-logic")
        })
      }
    })

    for (const roomKey of Object.keys(Logic.roomEls)) {
      Logic.roomEls[roomKey].classList.toggle(
        "room-has-available-item",
        roomsWithAvailableItems.has(roomKey),
      )
      Logic.roomEls[roomKey].classList.toggle(
        "room-has-available-quest",
        roomsWithAvailableQuests.has(roomKey) &&
          !roomsWithAvailableItems.has(roomKey),
      )
    }

    // Room-level grey overlay based on physical reachability
    if (roomGraph) {
      for (const roomKey of Object.keys(Logic.roomEls)) {
        const el = Logic.roomEls[roomKey]
        el.classList.remove("room-unreachable", "room-partial")
        const st = roomGraph.roomStatus(roomKey)
        if (st === "none") el.classList.add("room-unreachable")
        else if (st === "partial") el.classList.add("room-partial")
      }
    }
  }
}
window.onApConnect.push(() => {
  Logic.REAL_ITEM_NAMES = new Set(
    Object.values(ap.slotData.AP_ITEM_IDS),
  )
  document
    .querySelectorAll(".progression-icon[data-location]")
    .forEach((el) => {
      // ANCHOR exclude some icons from prog checks
      if (["area:", "flag:"].find((e) => el.alt.startsWith(e))) {
        return
      }
      ;(Logic.iconsByLocation[el.dataset.location] ||= []).push(el)
    })
  document
    .querySelectorAll(
      '.tile-wrapper[data-room]:not([data-room="20_16"])',
    )
    .forEach((el) => {
      Logic.roomEls[el.dataset.room] = el
    })
})
window.onApCreated.push((ap) => {
  const origOnReceivedItems = ap.onReceivedItems.bind(ap)
  ap.onReceivedItems = function (packet) {
    origOnReceivedItems(packet)
    if (!window.playerLoaded) return
    packet.items.forEach((item) => {
      let name = ap.slotData.AP_ITEM_IDS[item.item]
      if (name) {
        switch (name) {
          case "weapon:progressive weapons":
            name = [
              "weapon:aSword",
              "weapon:club",
              "weapon:dagger",
              "weapon:sword",
              "weapon:sKnife",
              "weapon:pitchfork",
              "weapon:warlockStaff",
              "weapon:royalStaff",
              "weapon:royalSword",
              "weapon:sunSword",
              "weapon:shadowStaff",
              "weapon:refreshStaff",
              "weapon:orcBlade",
              "weapon:creeperCrusher",
              "weapon:twinFury",
              "weapon:baneBlade",
              "weapon:axe",
              "weapon:bombSword",
              "weapon:soulSword",
            ][this.pwcount++]
            break
          case "armor:progressive armor":
            name = [
              "armor:alphaArmor",
              "armor:vest",
              "armor:regenArmor",
              "armor:robe",
              "armor:iron",
              "armor:mysticCloak",
              "armor:sunArmor",
              "armor:royalArmor",
              "armor:phantomCoat",
              "armor:speedVest",
              "armor:soulArmor",
              "armor:shadowCoat",
              "armor:grimGear",
              "armor:nobleArmor",
              "armor:diamondArmor",
            ][this.pacount++]
            break
          case "magic:progressive magic":
            name = [
              "magic:slow",
              "magic:crush",
              "magic:blast",
              "magic:heal",
              "magic:fire",
              "magic:weak",
              "magic:blessing",
              "magic:drain",
              "magic:cloud",
              "magic:regen",
              "magic:refresh",
              "magic:doubleDown",
              "magic:ice",
              "magic:lightning",
            ][this.pmcount++]
            break
        }
        // TODO ???, now both equal figure ho to fix
        if (name == "permit:bomb.2") haveReal.add("permit:bomb")
        haveReal.add(name)
      }
    })
    Logic.recompute()
    window.onApConnect.push(function (packet) {
      Logic.recompute()
    })

    Logic.recompute()
    console.log(
      `[logic] reachability engine ready: ${PROG_DATA.length} entries`,
    )
  }
})
