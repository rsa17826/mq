// Item/Quest browser panel.
//
// Lists every PROG_DATA entry (location, requires, receive) with a "Track"
// button that points the map's path arrow at it (via map.js's trackToken,
// which itself now understands both quests and items, resolves area:*
// redirects out of the virtual "20_20" room, and falls back to a direct
// pointer arrow when there's no walkable route yet). Entries gated behind
// loot:* requirements also get a "Track Loot" button that surfaces the
// still-outstanding loot counts on the in-game HUD via window.extraData,
// without touching the path arrow.
//
// Requires PROG_DATA (prog.js), ap.slotData.AP_ITEM_IDS, and map.js's
// trackToken/applyLootTrackingFor to already be present on the page.

;(function () {
  function init() {
    if (
      !window.ap?.slotData?.AP_LOCATION_IDS ||
      typeof PROG_DATA === "undefined" ||
      !window.trackToken
    ) {
      setTimeout(init, 250)
      return
    }

    const REAL_ITEM_NAMES = new Set(
      Object.values(ap.slotData.AP_ITEM_IDS),
    )

    function baseTok(tok) {
      return String(tok).split("#")[0]
    }

    function isLootToken(tok) {
      return baseTok(tok).startsWith("loot:")
    }

    function fmtRequires(requires) {
      if (!requires || !requires.length) return "(none)"
      return requires
        .map((group) =>
          group.length ? group.map(String).join(" & ") : "(free)",
        )
        .join("  OR  ")
    }

    function fmtReceive(receive) {
      return (receive || []).map(String).join(", ") || "(nothing)"
    }

    // Token to hand to trackToken() for a given entry: quest receive
    // tokens ("quest:name.N") track by quest name so tracking auto-advances
    // through later points of the same quest; everything else tracks the
    // exact token.
    function primaryTrackToken(entry) {
      const questTok = (entry.receive || [])
        .map(baseTok)
        .find((t) => t.startsWith("quest:"))
      if (questTok) {
        const m = questTok.match(/^quest:(.+)\.\d+$/)
        return m ? `quest:${m[1]}` : questTok
      }
      const realTok = (entry.receive || [])
        .map(baseTok)
        .find((t) => REAL_ITEM_NAMES.has(t))
      if (realTok) return realTok
      return baseTok((entry.receive || [])[0] || "")
    }

    function entryLootTokens(entry) {
      const seen = new Map()
      ;(entry.requires || []).forEach((group) =>
        group.forEach((rawTok) => {
          if (!isLootToken(rawTok)) return
          const m = baseTok(rawTok).match(/^loot:([^#]+)#?(\d*)$/)
          if (!m) return
          const name = m[1]
          const count = m[2] ? Number(m[2]) : 1
          if (!seen.has(name) || seen.get(name) < count)
            seen.set(name, count)
        }),
      )
      return [...seen.entries()]
    }

    // --- Loot tracking accumulation ---
    // Clicking "Track Loot" on an entry no longer replaces whatever was
    // being shown on the HUD; instead we remember every entry that's been
    // loot-tracked and re-merge all of their loot requirements (summing
    // counts per loot name) every time a new one is added, so e.g.
    // loot:oArm#1 + loot:oArm#3 shows up as a single oArm 0/4 line instead
    // of two separate oArm 0/1 / oArm 0/3 lines.
    const trackedLootEntries = new Map()

    function entryKey(entry) {
      return `${entry.room}||${(entry.receive || []).join(",")}`
    }

    function computeMergedLootTotals() {
      const totals = new Map()
      trackedLootEntries.forEach((entry) => {
        entryLootTokens(entry).forEach(([name, count]) => {
          totals.set(name, (totals.get(name) || 0) + count)
        })
      })
      return totals
    }

    function applyMergedLootTracking(entry) {
      trackedLootEntries.set(entryKey(entry), entry)
      const totals = computeMergedLootTotals()
      const mergedEntry = {
        room: "Tracked Loot",
        requires: [
          [...totals.entries()].map(
            ([name, count]) => `loot:${name}#${count}`,
          ),
        ],
        receive: [],
      }
      window.applyLootTrackingFor(mergedEntry)
    }

    function clearLootTracking() {
      trackedLootEntries.clear()
      window.applyLootTrackingFor({ room: "Tracked Loot", requires: [[]], receive: [] })
    }

    // --- Subgroup classification ---
    // Every entry falls into exactly one subgroup: "Flags" for anything
    // gated behind a flag: requirement, "Quest: <name>" for entries that
    // receive a quest:<name>.N token (grouping all points of the same
    // questline together), or "Other" for everything else.
    function groupKeyFor(entry) {
      const hasFlag = (entry.requires || []).some((group) =>
        group.some((tok) => baseTok(tok).startsWith("flag:")),
      )
      if (hasFlag) return { key: "flags", label: "Flags" }

      const questTok = (entry.receive || [])
        .map(baseTok)
        .find((t) => t.startsWith("quest:"))
      if (questTok) {
        const m = questTok.match(/^quest:([^.]+)/)
        const name = m ? m[1] : questTok
        return { key: `quest:${name}`, label: `Quest: ${name}` }
      }

      return { key: "other", label: "Other" }
    }

    // Persisted across re-renders so toggling a subgroup open/closed
    // survives the periodic refresh and filter typing. Undefined/absent
    // means "collapsed" (matches the main panel's default state).
    const groupCollapsed = new Map()

    function isChecked(entry) {
      const tok = baseTok((entry.receive || [])[0] || "")
      if (!tok) return false
      const key = `${entry.room} - ${tok}`
      const els = document.querySelectorAll(
        `.progression-icon[data-location="${CSS.escape(key)}"]`,
      )
      return (
        [...els].some((el) => el.classList.contains("checked")) ||
        (tok.startsWith("quest:") &&
          typeof QuestState !== "undefined" &&
          QuestState.satisfied(tok))
      )
    }

    // --- Panel scaffolding ---

    const style = document.createElement("style")
    style.textContent = `
      #item-tracker-panel button {
        background: #333;
        color: #eee;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 2px 8px;
        cursor: pointer;
        font-family: monospace;
        font-size: 11px;
      }
      #item-tracker-panel button:hover { background: #454545; }
      #item-tracker-panel input[type="text"] {
        width: 100%;
        box-sizing: border-box;
        background: #111;
        color: #eee;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 4px 6px;
        font-family: monospace;
        font-size: 11px;
        margin: 6px 0;
      }
    `
    document.head.appendChild(style)

    const panel = document.createElement("div")
    panel.id = "item-tracker-panel"
    panel.style.cssText = `
      position: absolute;
      top: 20px;
      right: 350px;
      max-height: 70vh;
      width: 380px;
      overflow-y: auto;
      background: rgba(20,20,20,0.94);
      border: 1px solid #444;
      border-radius: 8px;
      padding: 10px 12px;
      font-family: monospace;
      font-size: 11px;
      color: #e0e0e0;
      z-index: 10000000;
    `

    const header = document.createElement("div")
    header.style.cssText =
      "display:flex; justify-content:space-between; align-items:center; cursor:pointer;"
    header.innerHTML = `<b>Items &amp; Quests</b><span id="item-tracker-toggle">▾</span>`

    const filterInput = document.createElement("input")
    filterInput.type = "text"
    filterInput.placeholder =
      "Filter by room, requires, or receive..."

    const clearLootBtn = document.createElement("button")
    clearLootBtn.textContent = "Clear Loot Tracking"
    clearLootBtn.style.cssText = "margin-bottom:6px;"
    clearLootBtn.title = "Reset the merged loot HUD (all Track Loot selections)"
    clearLootBtn.onclick = (e) => {
      e.stopPropagation()
      clearLootTracking()
    }

    const body = document.createElement("div")
    const list = document.createElement("div")
    list.id = "item-tracker-list"
    body.appendChild(filterInput)
    body.appendChild(clearLootBtn)
    body.appendChild(list)

    panel.appendChild(header)
    panel.appendChild(body)
    document.getElementById("viewport")?.appendChild(panel)

    header.addEventListener("click", () => {
      const hidden = body.style.display === "none"
      body.style.display = hidden ? "" : "none"
      header.querySelector("#item-tracker-toggle").textContent =
        hidden ? "▾" : "▸"
    })
    body.style.display = "none"
    header.querySelector("#item-tracker-toggle").textContent = "▸"

    filterInput.addEventListener("click", (e) => e.stopPropagation())
    filterInput.addEventListener("input", (e) => {
      e.stopPropagation()
      render()
    })

    function buildEntryRow(entry) {
      const reqStr = fmtRequires(entry.requires)
      const recStr = fmtReceive(entry.receive)

      const row = document.createElement("div")
      row.style.cssText =
        "border-bottom:1px solid #333; padding:6px 0; display:flex; flex-direction:column; gap:2px;"

      if (isChecked(entry)) row.style.opacity = "0.4"

      const loc = document.createElement("div")
      loc.innerHTML = `<b>${entry.room}</b>`
      const req = document.createElement("div")
      req.textContent = `Requires: ${reqStr}`
      req.style.color = "#aaa"
      const rec = document.createElement("div")
      rec.textContent = `Receive: ${recStr}`
      rec.style.color = "#8f8"

      row.appendChild(loc)
      row.appendChild(req)
      row.appendChild(rec)

      const btnRow = document.createElement("div")
      btnRow.style.cssText = "display:flex; gap:6px; margin-top:4px;"

      const trackBtn = document.createElement("button")
      trackBtn.textContent = "Track"
      trackBtn.title =
        "Point the map arrow here (and auto-surface any outstanding loot requirement)"
      trackBtn.onclick = (e) => {
        e.stopPropagation()
        window.trackToken(primaryTrackToken(entry))
      }
      btnRow.appendChild(trackBtn)

      const lootTokens = entryLootTokens(entry)
      if (lootTokens.length) {
        const lootBtn = document.createElement("button")
        lootBtn.textContent = "Track Loot"
        lootBtn.title =
          "Merge this entry's outstanding loot counts into the HUD (adds to, rather than replaces, any loot already being tracked)"
        lootBtn.onclick = (e) => {
          e.stopPropagation()
          applyMergedLootTracking(entry)
        }
        btnRow.appendChild(lootBtn)
      }

      row.appendChild(btnRow)
      return row
    }

    function render() {
      const q = filterInput.value.trim().toLowerCase()
      list.innerHTML = ""

      const groups = new Map() // key -> { label, entries: [] }

      PROG_DATA.forEach((entry) => {
        const reqStr = fmtRequires(entry.requires)
        const recStr = fmtReceive(entry.receive)
        if (
          q &&
          !`${entry.room} ${reqStr} ${recStr}`
            .toLowerCase()
            .includes(q)
        )
          return

        if (isChecked(entry) || /^(?:area|loot):/.test(recStr)) return

        const { key, label } = groupKeyFor(entry)
        if (!groups.has(key)) groups.set(key, { label, entries: [] })
        groups.get(key).entries.push(entry)
      })

      // Flags first, then questlines alphabetically, then Other last.
      const sortedKeys = [...groups.keys()].sort((a, b) => {
        if (a === "flags") return -1
        if (b === "flags") return 1
        if (a === "other") return 1
        if (b === "other") return -1
        return a.localeCompare(b)
      })

      sortedKeys.forEach((key) => {
        const group = groups.get(key)
        if (!group.entries.length) return

        const collapsed = groupCollapsed.has(key)
          ? groupCollapsed.get(key)
          : true

        const groupHeader = document.createElement("div")
        groupHeader.style.cssText =
          "display:flex; justify-content:space-between; align-items:center; cursor:pointer; background:#2a2a2a; padding:4px 6px; margin-top:6px; border-radius:4px; font-weight:bold;"
        groupHeader.innerHTML = `<span>${group.label} (${group.entries.length})</span><span>${
          collapsed ? "▸" : "▾"
        }</span>`
        groupHeader.addEventListener("click", (e) => {
          e.stopPropagation()
          groupCollapsed.set(key, !collapsed)
          render()
        })
        list.appendChild(groupHeader)

        if (collapsed) return

        const groupBody = document.createElement("div")
        groupBody.style.cssText = "padding-left:4px;"
        group.entries.forEach((entry) => {
          groupBody.appendChild(buildEntryRow(entry))
        })
        list.appendChild(groupBody)
      })
    }

    render()
    window.__itemTrackerRefresh = render

    // Cheap periodic refresh so "checked" dimming stays roughly current
    // without deep-observing the whole map DOM.
    setInterval(render, 3000)

    console.log(
      `[item-tracker] panel ready: ${PROG_DATA.length} entries`,
    )
  }

  init()
})()
