// Basic Archipelago map tracking.
// Assumes this script loads AFTER apClient.js and the game's
// ap.slotData.AP_LOCATION_IDS / ap.slotData.AP_ITEM_IDS globals are defined on the page,
// and that window.ap is (or will be) the connected ArchipelagoClient.

;(function () {
  function init() {
    if (!window.ap?.slotData?.AP_LOCATION_IDS) {
      setTimeout(init, 250)
      return
    }

    // id -> "north_east - item" location key
    const ID_TO_LOCATION = {}
    for (const key in ap.slotData.AP_LOCATION_IDS) {
      ID_TO_LOCATION[ap.slotData.AP_LOCATION_IDS[key]] = key
    }

    // Cache icon elements by location key for fast lookups
    const iconsByLocation = {}
    document
      .querySelectorAll(".progression-icon[data-location]")
      .forEach((el) => {
        const key = el.dataset.location
        ;(iconsByLocation[key] ||= []).push(el)
      })

    function markChecked(locationId) {
      const key = ID_TO_LOCATION[locationId]
      if (!key) return
      const els = iconsByLocation[key]
      if (!els) return
      els.forEach((el) => el.classList.add("checked"))
    }

    function syncCheckedLocations(list) {
      if (!list) return
      list.forEach(markChecked)
    }

    // --- Locations: initial sync + ongoing updates ---
    const origOnConnected = ap.onConnected.bind(ap)
    ap.onConnected = function (packet) {
      origOnConnected(packet)
      if (window.playerLoaded) {
        syncCheckedLocations(ap.checkedLocations)
      } else {
        window.onPlayerLoaded.push(() => {
          syncCheckedLocations(ap.checkedLocations)
        })
      }
    }

    const origOnRoomUpdate = ap.onRoomUpdate.bind(ap)
    ap.onRoomUpdate = function (packet) {
      origOnRoomUpdate(packet)
      syncCheckedLocations(packet.checked_locations)
    }

    // In case connection happened before this script attached its hooks
    if (ap.checkedLocations) syncCheckedLocations(ap.checkedLocations)

    // --- Items: basic received-item counter panel ---
    const itemCounts = {}
    const panel = document.createElement("div")
    panel.id = "tracker-item-panel"
    panel.style.cssText = `
      position: absolute;
      bottom: 20px;
      right: 20px;
      max-height: 40vh;
      width: 260px;
      overflow-y: auto;
      background: rgba(20,20,20,0.92);
      border: 1px solid #444;
      border-radius: 8px;
      padding: 10px 12px;
      font-family: monospace;
      font-size: 12px;
      color: #e0e0e0;
      z-index: 10000000;
    `
    panel.innerHTML =
      "<b>Items received</b><div id='tracker-item-list'></div>"
    document.getElementById("viewport")?.appendChild(panel)

    function renderItemPanel() {
      const list = document.getElementById("tracker-item-list")
      if (!list) return
      const rows = Object.entries(itemCounts)
        .sort((a, b) => a[0].localeCompare(b[0]))
        .map(
          ([name, count]) =>
            `<div>${name}${count > 1 ? ` x${count}` : ""}</div>`,
        )
        .join("")
      list.innerHTML = rows
    }

    const origOnReceivedItems = ap.onReceivedItems.bind(ap)
    ap.onReceivedItems = function (packet) {
      origOnReceivedItems(packet)
      if (window.playerLoaded) {
        packet.items.forEach((item) => {
          const name =
            ap.slotData.AP_ITEM_IDS[item.item] || `#${item.item}`
          itemCounts[name] = (itemCounts[name] || 0) + 1
        })
        renderItemPanel()
      }
    }

    console.log(
      "[tracker] hooked into Archipelago client for map tracking",
    )
  }

  init()
})()
