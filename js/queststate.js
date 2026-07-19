// Shared quest-value state, used by both roomgraph.js and logic.js to
// resolve "quest:name.value" tokens (threshold comparisons, not simple
// have/have-not flags).

class QuestState {
  /** @type {Record<string, number>} */
  static values = {} // questName -> current numeric value

  /**
   *
   * @param {string} tok
   * @returns
   */
  static parseToken(tok) {
    // e.g. "quest:curse.5" -> { name: "curse", threshold: 5 }
    const m = tok.match(/^quest:(.+)\.(-?\d+)$/)
    if (!m) return null
    return { name: m[1], threshold: Number(m[2]) }
  }

  /**
   *
   * @param {string} tok
   * @returns
   */
  static satisfied(tok) {
    const p = QuestState.parseToken(tok)
    if (!p) return false
    const v = QuestState.values[p.name]
    return v !== undefined && v >= p.threshold
  }

  /**
   *
   * @param {string} name
   * @param {number} value
   */
  static set(name, value) {
    QuestState.values[name] = value
  }

  // Read current values straight from the game's manager.quest, keyed by
  // Enum.Quest so names line up with the "quest:name.value" token format.
  static seedFromGame() {
    for (const key of Object.keys(Enum.Quest)) {
      const v = manager.quest[Enum.Quest[key]]
      if (v !== undefined) QuestState.values[key] = v
    }
  }
}
