// Shared quest-value state, used by both roomgraph.js and logic.js to
// resolve "quest:name.value" tokens (threshold comparisons, not simple
// have/have-not flags).

const QuestState = (function () {
  const values = {} // questName -> current numeric value

  function parseToken(tok) {
    // e.g. "quest:curse.5" -> { name: "curse", threshold: 5 }
    const m = tok.match(/^quest:(.+)\.(-?\d+)$/)
    if (!m) return null
    return { name: m[1], threshold: Number(m[2]) }
  }

  function satisfied(tok) {
    const p = parseToken(tok)
    if (!p) return false
    const v = values[p.name]
    return v !== undefined && v >= p.threshold
  }

  function set(name, value) {
    values[name] = value
  }

  // Read current values straight from the game's manager.quest, keyed by
  // Enum.Quest so names line up with the "quest:name.value" token format.
  function seedFromGame() {
    for (const key of Object.keys(Enum.Quest)) {
      try {
        const v = manager.quest[Enum.Quest[key]]
        if (v !== undefined) values[key] = v
      } catch (e) {
        // ignore keys that don't resolve cleanly
      }
    }
  }

  return { satisfied, set, seedFromGame, values }
})()

// The game calls this whenever a quest value changes.
window.onQuestChanged = function (prop, value) {
  // does nothing as the values get repulled
  // QuestState.set(prop, value)
  window.__trackerRecompute?.()
}
