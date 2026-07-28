// global.d.ts
export {}

declare global {
  interface Window {
    ap: ArchipelagoClient
    onPlayerLoaded: Array<() => void>
    apErrors: string[]
    onApConnect: Array<() => void>
    onApCreated: Array<(ap: any) => void>
    onQuestChanged: Array<(name: number, val: number) => void>
    onNewScreen: Array<() => void>
    log: (...a) => void
    warn: (...a) => void
    error: (...a) => void
    trace: (...a) => void
    group: (...a) => void
    groupEnd: (...a) => void
    table: (...a) => void
  }

  var ap: ArchipelagoClient
  var log: (...a) => void
  var warn: (...a) => void
  var error: (...a) => void
  var trace: (...a) => void
  var group: (...a) => void
  var groupEnd: (...a) => void
  var table: (...a) => void

  var apLog: (...a) => void
  var apWarn: (...a) => void
  var apError: (...a) => void
}
