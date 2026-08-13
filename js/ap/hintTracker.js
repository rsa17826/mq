class HintTracker {
  static all = []

  static setHints(list) {
    HintTracker.all = list
    HintTracker.render()
  }

  // Items you'll receive, hinted anywhere in the multiworld
  static get incoming() {
    return HintTracker.all.filter(
      (h) => h.receiving_player === ap.slot,
    )
  }

  // Locations that physically live in your world (any receiving player)
  static get inMyGame() {
    return HintTracker.all.filter((h) => h.finding_player === ap.slot)
  }

  static render() {
    // e.g. resolve item/location names via ap.getItemName / ap.locationIdToName[game][id],
    // then split into two panel lists using .found for checked/unchecked styling
  }
}
