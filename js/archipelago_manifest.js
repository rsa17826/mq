const ROOM_INTERNAL_WIDTH = 710.0
const ROOM_INTERNAL_HEIGHT = 560.0
const BLOCKS_X = 14
const BLOCKS_Y = 11
const BLOCK_W = ROOM_INTERNAL_WIDTH / BLOCKS_X
const BLOCK_H = ROOM_INTERNAL_HEIGHT / BLOCKS_Y

var ER_MAP = new Map()
window.ER_MAP = ER_MAP

function onRoomDataLoaded() {
  for (var r of window.ap.slotData.roomData) {
    // Key by origin room: "north_east"
    var key = r[0] + "_" + r[1]
    if (!ER_MAP.has(key)) {
      ER_MAP.set(key, [])
    }
    ER_MAP.get(key).push({
      origSide: r[2],
      origIdx: r[3],
      newNorth: r[4],
      newEast: r[5],
      exitSide: r[6],
      exitIdx: r[7],
    })
  }
  ap.sendLocationScouts(Object.values(ap.slotData.AP_LOCATION_IDS), 0)
  console.log(
    `[Archipelago] Database ready: ${Object.keys(ap.slotData.AP_LOCATION_IDS).length} locations, ${Object.keys(ap.slotData.AP_ITEM_IDS).length} items, ${Object.keys(ap.slotData.AP_ENTRANCE_IDS).length} entrances.`,
  )
}
