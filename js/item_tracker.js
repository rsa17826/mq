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

class ItemTracker {
  static groupCollapsed = new Map()
  static inLogicOnly = true
  static trackedLootEntries = new Map()
  /** @type {Set<string>} */
  static REAL_ITEM_NAMES = new Set()
  /**
   * @param {string} tok
   * @returns {string}
   */
  static baseTok(tok) {
    return String(tok).split("#")[0]
  }

  /**
   * @param {string} tok
   * @returns {boolean}
   */
  static isLootToken(tok) {
    return this.baseTok(tok).startsWith("loot:")
  }

  /**
   * @param {string[][]} requires
   * @returns {string}
   */
  static fmtRequires(requires) {
    if (!requires || !requires.length) return "(none)"
    return requires
      .map((group) =>
        group.length ? group.map(String).join(" & ") : "(free)",
      )
      .join("  OR  ")
  }

  /**
   * @param {string[]|undefined} receive
   * @returns {string}
   */
  static fmtReceive(receive) {
    return (receive || []).map(String).join(", ") || "(nothing)"
  }

  // Token to hand to trackToken() for a given entry: quest receive
  // tokens ("quest:name.N") track by quest name so tracking auto-advances
  // through later points of the same quest; everything else tracks the
  // exact token.
  /**
   * @param {Entry} entry
   * @returns {string}
   */
  static primaryTrackToken(entry) {
    const questTok = (entry.receive || [])
      .map((t) => this.baseTok(t))
      .find((t) => t.startsWith("quest:"))
    if (questTok) {
      const m = questTok.match(/^quest:(.+)\.\d+$/)
      return m ? `quest:${m[1]}` : questTok
    }
    const realTok = (entry.receive || [])
      .map((t) => this.baseTok(t))
      .find((t) => this.REAL_ITEM_NAMES.has(t))
    if (realTok) return realTok
    return this.baseTok((entry.receive || [])[0] || "")
  }

  static entryLootTokens(entry) {
    const seen = new Map()
    ;(entry.requires || []).forEach((group) =>
      group.forEach((rawTok) => {
        if (!this.isLootToken(rawTok)) return
        const m = this.baseTok(rawTok).match(/^loot:([^#]+)#?(\d*)$/)
        if (!m) return
        const name = m[1]
        const count = m[2] ? Number(m[2]) : 1
        if (!seen.has(name) || seen.get(name) < count)
          seen.set(name, count)
      }),
    )
    return [...seen.entries()]
  }

  static entryKey(entry) {
    return `${entry.room}||${(entry.receive || []).join(",")}`
  }

  static computeMergedLootTotals() {
    const totals = new Map()
    this.trackedLootEntries.forEach((entry) => {
      this.entryLootTokens(entry).forEach(([name, count]) => {
        totals.set(name, (totals.get(name) || 0) + count)
      })
    })
    return totals
  }

  static applyMergedLootTracking(entry) {
    this.trackedLootEntries.set(this.entryKey(entry), entry)
    const totals = this.computeMergedLootTotals()
    const mergedEntry = {
      room: "Tracked Loot",
      requires: [
        [...totals.entries()].map(
          ([name, count]) => `loot:${name}#${count}`,
        ),
      ],
      receive: [],
    }
    PathFinding.applyLootTrackingFor(mergedEntry)
  }

  static clearLootTracking() {
    this.trackedLootEntries.clear()
    PathFinding.applyLootTrackingFor({
      room: "Tracked Loot",
      requires: [[]],
      receive: [],
    })
  }

  // --- Subgroup classification ---
  // Every entry falls into exactly one subgroup: "Flags" for anything
  // gated behind a flag: requirement, "Quest: <name>" for entries that
  // receive a quest:<name>.N token (grouping all points of the same
  // questline together), or "Other" for everything else.
  static groupKeyFor(entry) {
    const hasFlag =
      (entry.requires || []).some((group) =>
        group.some((tok) => this.baseTok(tok).startsWith("flag:")),
      ) ||
      (entry.receive || []).every((tok) =>
        this.baseTok(tok).startsWith("flag:"),
      )
    if (hasFlag) return { key: "flags", label: "Flags" }

    const questTok = (entry.receive || [])
      .map((t) => this.baseTok(t))
      .find((t) => t.startsWith("quest:"))
    if (questTok) {
      const m = questTok.match(/^quest:([^.]+)/)
      const name = m ? m[1] : questTok
      return { key: `quest:${name}`, label: `Quest: ${name}` }
    }

    return { key: "other", label: "Other" }
  }

  static isChecked(entry) {
    const tok = this.baseTok((entry.receive || [])[0] || "")
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

  // "In logic" per logic.js's classification: the entry's first receive
  // token's icon(s) carry the "in-logic" class it applies each recompute.
  // If no matching icon exists at all (e.g. the token isn't rendered as
  // an icon), treat it as in-logic so the filter doesn't silently hide it.
  static isInLogic(entry) {
    const tok = this.baseTok((entry.receive || [])[0] || "")
    if (!tok) return true
    const key = `${entry.room} - ${tok}`
    const els = document.querySelectorAll(
      `.progression-icon[data-location="${CSS.escape(key)}"]`,
    )
    if (!els.length) return true
    return [...els].some((el) => el.classList.contains("in-logic"))
  }

  // ---- UI construction ----

  static _buildUi() {
    document.getElementById("viewport").appendChild(
      (this.itemTrackerPanel = newelem(
        "div",
        { id: "item-tracker-panel" },
        [
          (this.header = newelem(
            "div",
            {
              position: "sticky",
              top: "-10px",
              zIndex: "10",
              background: "rgba(20, 20, 20, 0.98)",
              paddingBottom: "4px",
            },
            [
              newelem("div", { id: "header" }, [
                newelem("div", {}, [
                  newelem("b", {}, ["Items & Quests"]),
                  (this.itemTrackerToggle = newelem(
                    "span",
                    { id: "item-tracker-toggle" },
                    ["▾"],
                  )),
                ]),
                (this.filterInput = newelem("input", {
                  type: "text",
                  placeholder:
                    "Filter by room, requires, or receive...",
                })),
                (this.inLogicLabel = newelem(
                  "label",
                  {
                    display: "flex",
                    alignItems: "center",
                    gap: "4px",
                    fontSize: "18px",
                    color: "#ccc",
                    cursor: "pointer",
                    userSelect: "none",
                    margin: "4px 0",
                    onclick: (e) => {
                      e.stopPropagation()
                      e.stopImmediatePropagation()
                    },
                  },
                  [
                    (this.inLogicCheckbox = newelem("input", {
                      type: "checkbox",
                      checked: true,
                      onchange: (e) => {
                        e.stopPropagation()
                        e.stopImmediatePropagation()
                        this.inLogicOnly =
                          this.inLogicCheckbox.checked
                        this.render()
                      },
                    })),
                    "In logic only",
                  ],
                )),
                (this.clearLootBtn = newelem(
                  "button",
                  {
                    title:
                      "Reset the merged loot HUD (all Track Loot selections)",
                    onclick: (e) => {
                      e.stopPropagation()
                      this.clearLootTracking()
                    },
                  },
                  ["Clear Loot Tracking"],
                )),
              ]),
            ],
          )),
          (this.body = newelem("div", { id: "body" }, [
            (this.list = newelem("div", { id: "item-tracker-list" })),
          ])),
        ],
      )),
    )

    this.header.addEventListener("click", () => {
      const hidden = this.body.style.display === "none"
      this.body.style.display = hidden ? "" : "none"
      this.itemTrackerToggle.textContent = hidden ? "▾" : "▸"
    })
    this.body.style.display = "none"
    this.itemTrackerToggle.textContent = "▸"

    this.filterInput.addEventListener("keyup", (e) =>
      e.stopPropagation(),
    )
    this.filterInput.addEventListener("keydown", (e) =>
      e.stopPropagation(),
    )
    this.filterInput.addEventListener("click", (e) =>
      e.stopPropagation(),
    )
    this.filterInput.addEventListener("input", (e) => {
      e.stopPropagation()
      this.render()
    })
  }

  static buildEntryRow(entry) {
    const reqStr = this.fmtRequires(entry.requires)
    const recStr = this.fmtReceive(entry.receive)

    const row = newelem("div", { id: "item-tracker-row" }, [
      newelem("b", {}, [entry.room]),
      newelem("div", { color: "#aaa" }, [`Requires: ${reqStr}`]),
      newelem("div", { color: "#8f8" }, [`Receive: ${recStr}`]),
      newelem("div", { id: "btn-row" }, [
        newelem(
          "button",
          {
            title:
              "Point the map arrow here (and auto-surface any outstanding loot requirement)",
            onclick: (e) => {
              e.stopPropagation()
              WorldMap.trackToken(this.primaryTrackToken(entry))
            },
          },
          ["Track"],
        ),
        this.entryLootTokens(entry).length ?
          newelem(
            "button",
            {
              title:
                "Merge this entry's outstanding loot counts into the HUD (adds to, rather than replaces, any loot already being tracked)",
              onclick: (e) => {
                e.stopPropagation()
                this.applyMergedLootTracking(entry)
              },
            },
            ["Track Loot"],
          )
        : null,
      ]),
    ])

    if (this.isChecked(entry)) row.style.opacity = "0.4"
    return row
  }

  // ---- rendering ----

  static render() {
    const q = this.filterInput.value.trim().toLowerCase()
    this.list.innerHTML = ""

    const groups = new Map() // key -> { label, entries: [] }

    PROG_DATA.forEach((entry) => {
      const reqStr = this.fmtRequires(entry.requires)
      const recStr = this.fmtReceive(entry.receive)
      if (
        q &&
        !`${entry.room} ${reqStr} ${recStr}`.toLowerCase().includes(q)
      )
        return

      if (this.isChecked(entry) || /^(?:area|loot):/.test(recStr))
        return

      if (this.inLogicOnly && !this.isInLogic(entry)) return

      const { key, label } = this.groupKeyFor(entry)
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

      const collapsed =
        this.groupCollapsed.has(key) ?
          this.groupCollapsed.get(key)
        : true

      const groupHeader = document.createElement("div")
      groupHeader.style.cssText =
        "display:flex; justify-content:space-between; align-items:center; cursor:pointer; background:#2a2a2a; padding:4px 6px; margin-top:6px; border-radius:4px; font-weight:bold;"
      groupHeader.innerHTML = `<span>${group.label} (${group.entries.length})</span><span>${
        collapsed ? "▸" : "▾"
      }</span>`
      groupHeader.addEventListener("click", (e) => {
        e.stopPropagation()
        this.groupCollapsed.set(key, !collapsed)
        this.render()
      })
      this.list.appendChild(groupHeader)

      if (collapsed) return

      const groupBody = document.createElement("div")
      groupBody.style.cssText = "padding-left:4px;"
      group.entries.forEach((entry) => {
        groupBody.appendChild(this.buildEntryRow(entry))
      })
      this.list.appendChild(groupBody)
    })
  }
}

window.onApConnect.push(() => {
  ItemTracker.REAL_ITEM_NAMES = new Set(
    Object.values(ap.slotData.AP_ITEM_IDS),
  )
  ItemTracker._buildUi()
  window.onQuestChanged.push(() => {
    ItemTracker.render()
  })
  window.onPlayerLoaded.push(() => {
    ItemTracker.render()
  })
})
