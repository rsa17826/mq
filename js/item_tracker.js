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

    const body = document.createElement("div")
    const list = document.createElement("div")
    list.id = "item-tracker-list"
    body.appendChild(filterInput)
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

    function render() {
      const q = filterInput.value.trim().toLowerCase()
      list.innerHTML = ""

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

        const row = document.createElement("div")
        row.style.cssText =
          "border-bottom:1px solid #333; padding:6px 0; display:flex; flex-direction:column; gap:2px;"

        if (isChecked(entry) || /^(?:area|loot):/.test(recStr)) return
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
        btnRow.style.cssText =
          "display:flex; gap:6px; margin-top:4px;"

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
            "Show outstanding loot counts on the HUD without moving the path arrow"
          lootBtn.onclick = (e) => {
            e.stopPropagation()
            window.applyLootTrackingFor(entry)
          }
          btnRow.appendChild(lootBtn)
        }

        row.appendChild(btnRow)
        list.appendChild(row)
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
