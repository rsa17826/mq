const CACHE_NAME = "math-quest-v1"
const ASSETS = [
  "/MathQuest/play.base.html",
  "/css/main.css",
  "/MathQuest/fonts/BOOTERZZ.woff2",
  "/MathQuest/lib/howler.min.js",
  "/MathQuest/MathQuest.js",
  "/js/apClient.js",
  "/js/map.js",
  "/js/tracker.js",
  "/js/prog.js",
  "/js/queststate.js",
  "/js/roomgraph.js",
  "/js/logic.js",
  "/js/item_tracker.js",
  "/js/aplog.js",
  "/js/overlay.js",
]

// Install Service Worker and cache core assets
// self.addEventListener("install", (event) => {
//   event.waitUntil(
//     caches.open(CACHE_NAME).then((cache) => {
//       // Map through assets to catch the specific one failing
//       return Promise.all(
//         ASSETS.map((url) => {
//           return cache.add(url).catch((err) => {
//             console.error("❌ Failed to cache asset:", url, err)
//           })
//         }),
//       )
//     }),
//   )
// })

// // Cache-first strategy for loading assets
// self.addEventListener("fetch", (event) => {
//   event.respondWith(
//     caches.match(event.request).then((cachedResponse) => {
//       return cachedResponse || fetch(event.request)
//     }),
//   )
// })
