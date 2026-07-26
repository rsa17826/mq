function findDuplicateLocations(data) {
  const locationMap = {}

  // Group keys by their locationName
  for (const [key, item] of Object.entries(data)) {
    // Check if data array exists and has at least one element with locationName
    if (item?.data?.[0]?.[2]?.locationName) {
      const location = item.data[0][2].locationName

      if (!locationMap[location]) {
        locationMap[location] = []
      }
      locationMap[location].push(key)
    }
  }

  // Find and print duplicates
  let foundDuplicate = false
  for (const [location, keys] of Object.entries(locationMap)) {
    if (keys.length > 1) {
      foundDuplicate = true
      console.log(`📍 Location: "${location}"`)
      console.log(`   Keys: ${keys.join(", ")}\n`)
    }
  }

  if (!foundDuplicate) {
    console.log("No duplicate locationNames found.")
  }
}
onNewScreen.push(() => {
  if (window.chestedItemInfo[`${manager.north}_${manager.east}`])
    findDuplicateLocations(
      window.chestedItemInfo[`${manager.north}_${manager.east}`],
    )
})
