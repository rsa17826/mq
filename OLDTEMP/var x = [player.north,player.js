var x = [player.north,player.east]
if (typeof ER_MAP !== "undefined" || window.ER_MAP) {
  const mapInstance =
    typeof ER_MAP !== "undefined" ? ER_MAP : window.ER_MAP
  console.log(`=== Active Randomizer Routes for Room ${x.join(',')} ===`)

  mapInstance.forEach((conns, key) => {
    // Correct order: 13 (North) and 26 (East)
    if (key.startsWith(`${x[0]}_${x[1]}_`)) {
      console.log(`Outbound Exit -> Vanilla Path: [${key}]`, conns)
    }
    conns.forEach((c) => {
      if (c.newNorth === x[0] && c.newEast === x[1]) {
        console.log(
          `Inbound Entrance -> Lands Here from Vanilla Path [${key}]:`,
          c,
        )
      }
    })
  })
} else {
  console.log(
    "ER_MAP is not defined or initialized in this scope yet.",
  )
}
