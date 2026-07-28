class HTMLStorage {
  /** @type {(HTMLElement & { alt:string,dataset:{location:string} })[]} */
  static progressionIcon = []
  /** @type {(HTMLElement & { dataset: { room: string } })[]} */
  static tileWrapper = []
  /** @type {Record<string,HTMLElement>} */
  static TileByKey = {}
  /** @type {(HTMLElement & { dataset: { room: string } })[]} */
  static exitSquare = []
  /** @type {HTMLElement} */
  static apChatLog
}
document.addEventListener(
  "DOMContentLoaded",
  () => {
    document
      .querySelectorAll(
        '.tile-wrapper[data-room]:not([data-room="20_16"])',
      )
      .forEach((el) => {
        // @ts-ignore
        HTMLStorage.tileWrapper.push(el)
        // @ts-ignore
        HTMLStorage.TileByKey[el.dataset.room] = el
      })
    // @ts-ignore
    HTMLStorage.exitSquare = [
      ...document.querySelectorAll(".exit-square"),
    ]
    // @ts-ignore
    HTMLStorage.progressionIcon = [
      ...document.querySelectorAll(".progression-icon"),
    ]
    // @ts-ignore
    HTMLStorage.apChatLog = document.querySelector("#apChatSayInput")
  },
  true,
)
