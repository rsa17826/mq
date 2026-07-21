// @ts-nocheck

// ---- Archipelago chat/log overlay -------------------------------------
// Buffers entries until the DOM element exists, then renders live.
// Wraps log/warn/error (which apClient.js already calls for every
// connection, item, and chat event) so nothing in apClient.js needs to
// change - everything it logs to the console also shows in the overlay.
window._apChatBuffer = []
window._apChatLogEl = null

function _apStringify(a) {
  if (typeof a === "string") return a
  if (a instanceof Error) return a.message
  try {
    return JSON.stringify(a)
  } catch (e) {
    return String(a)
  }
}

function _apRenderEntry(entry) {
  var el = document.createElement("div")
  el.innerHTML =
    "<span>[" + htmlesc(entry.time) + "] </span>" + entry.msg
  el.className = "ap-chat-entry ap-chat-" + entry.type
  entry.el = el // kept so the collapsed "toast" fade loop can update it
  window._apChatLogEl.appendChild(el)
  while (window._apChatLogEl.children.length > 200) {
    window._apChatLogEl.removeChild(window._apChatLogEl.firstChild)
  }
  window._apChatLogEl.scrollTop = window._apChatLogEl.scrollHeight
}

function htmlesc(str) {
  return str.replaceAll("&", "&amp;").replaceAll("<", "&lt;")
}
function parseatts(str, type) {
  const regex = /(@\w*!)/g
  const result = str.split(regex).filter(Boolean)

  let html = "<span>"
  let inspan = false
  let inconsole = false

  // Variables for console styling
  let consoleLogStr = ""
  let consoleStyles = []
  let currentConsoleColor = "color: inherit" // Default fallback color

  for (var part of result) {
    switch (part) {
      case "@red!":
        if (inspan) html += "</span>"
        html += '<span style="color:red">'
        inspan = true

        // Track style for console
        currentConsoleColor = "color: red"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@blue!":
        if (inspan) html += "</span>"
        html += '<span style="color:skyblue">'
        inspan = true

        currentConsoleColor = "color: skyblue"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@green!":
        if (inspan) html += "</span>"
        html += '<span style="color:lightgreen">'
        inspan = true

        currentConsoleColor = "color: lightgreen"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@darkgrey!":
        if (inspan) html += "</span>"
        html += '<span style="color:darkgrey">'
        inspan = true

        currentConsoleColor = "color: darkgrey"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@grey!":
        if (inspan) html += "</span>"
        html += '<span style="color:grey">'
        inspan = true

        currentConsoleColor = "color: grey"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@darkorange!":
        if (inspan) html += "</span>"
        html += '<span style="color:darkorange">'
        inspan = true

        currentConsoleColor = "color: darkorange"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@orange!":
        if (inspan) html += "</span>"
        html += '<span style="color:orange">'
        inspan = true

        currentConsoleColor = "color: orange"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@hotpink!":
        if (inspan) html += "</span>"
        html += '<span style="color:hotpink">'
        inspan = true

        currentConsoleColor = "color: hotpink"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@cyan!":
        if (inspan) html += "</span>"
        html += '<span style="color:cyan">'
        inspan = true

        currentConsoleColor = "color: cyan"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@yellow!":
        if (inspan) html += "</span>"
        html += '<span style="color:yellow">'
        inspan = true

        currentConsoleColor = "color: yellow"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@brown!":
        if (inspan) html += "</span>"
        html += '<span style="color:brown">'
        inspan = true

        currentConsoleColor = "color: brown"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@pink!":
        if (inspan) html += "</span>"
        html += '<span style="color:pink">'
        inspan = true

        currentConsoleColor = "color: pink"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@purple!":
        if (inspan) html += "</span>"
        html += '<span style="color:purple">'
        inspan = true

        currentConsoleColor = "color: purple"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      case "@console!":
        inconsole = true
        break
      case "@!":
        if (inspan) html += "</span>"
        inspan = false
        inconsole = false

        // Reset console color back to normal
        currentConsoleColor = "color: inherit"
        consoleLogStr += "%c"
        consoleStyles.push(currentConsoleColor)
        break
      default:
        if (!inconsole) html += htmlesc(owo(part))
        consoleLogStr += owo(part)
    }
  }

  html += "</span>"

  // Use the spread operator (...) to pass the styles array as individual arguments
  console[type](consoleLogStr, ...consoleStyles)

  return html
}

window.apLog = function apLog(...args) {
  apChatLogRaw(
    parseatts(args.map(_apStringify).join(" "), "log"),
    "log",
  )
}
window.apWarn = function apWarn(...args) {
  apChatLogRaw(
    parseatts(args.map(_apStringify).join(" "), "warn"),
    "warn",
  )
}
window.apError = function apError(...args) {
  window.apErrors.push(args.map(_apStringify).join(" "))
  apChatLogRaw(
    parseatts(args.map(_apStringify).join(" "), "error"),
    "error",
  )
}

function apChatLogRaw(msg, type) {
  var entry = {
    msg: String(msg),
    type: type || "log",
    time:
      localStorage.timeFormat ?
        new Date().toLocaleTimeString(undefined, {
          hour12: localStorage.timeFormat == "12",
        })
      : new Date().toLocaleTimeString(),
    createdAt: Date.now(), // used for the collapsed "toast" fade timing
  }
  window._apChatBuffer.push(entry)
  if (window._apChatBuffer.length > 200) window._apChatBuffer.shift()
  if (window._apChatLogEl) _apRenderEntry(entry)
  _apUpdateToastOpacities()
}

// ---- Collapsed "toast" behavior ----------------------------------------
// While the log is collapsed, recent messages (< 5s old) still show,
// fading out linearly over their last 1s of life, instead of the log
// being fully hidden. The say/input row stays hidden regardless.
var AP_TOAST_LIFETIME_MS = 5000
var AP_TOAST_FADE_MS = 1000

function _apUpdateToastOpacities() {
  var container = document.getElementById("apChatLogContainer")
  if (!container) return
  var now = Date.now()
  var fadeStart = AP_TOAST_LIFETIME_MS - AP_TOAST_FADE_MS
  var oneVisible = false
  window._apChatBuffer.forEach(function (entry) {
    if (!entry.el) return
    if (!container.classList.contains("collapsed")) {
      entry.el.style.display = "block"
      return
    }
    var age = now - entry.createdAt
    if (age >= AP_TOAST_LIFETIME_MS) {
      entry.el.style.display = "none"
    } else {
      entry.el.style.display = "block"
      oneVisible = true
      entry.el.style.opacity =
        age <= fadeStart ? "1" : (
          String(1 - (age - fadeStart) / AP_TOAST_FADE_MS)
        )
    }
  })
  if (oneVisible) {
    setTimeout(_apUpdateToastOpacities, 100)
  }
  document.querySelector("#apChatLog").style.display =
    oneVisible || !container.classList.contains("collapsed") ?
      "block"
    : "none"
}

function _apResetEntryStyles() {
  window._apChatBuffer.forEach(function (entry) {
    if (!entry.el) return
    entry.el.style.display = ""
    entry.el.style.opacity = ""
  })
  // _apUpdateToastOpacities can leave #apChatLog itself pinned to
  // display:none (when collapsed with nothing currently visible) -
  // clear that too, or expanding the log later shows nothing.
  var logEl = document.getElementById("apChatLog")
  if (logEl) {
    logEl.style.display = ""
  }
}

window._apUpdateToastOpacities = _apUpdateToastOpacities
window._apResetEntryStyles = _apResetEntryStyles
window._apChatLogEl = document.getElementById("apChatLog")
window._apChatBuffer.forEach(_apRenderEntry)

function apSendSayFromInput() {
  var input = document.getElementById("apChatSayInput")
  var text = input.value.trim()
  text = text.replace(/^!giveitem /, "!getitem ")
  const options = {
    help: {
      alias: ["?"],
      desc: "shows available commands",
      func() {
        var logtext =
          "@purple!===============@! @pink!COMMAND LIST@! @purple!===============@!\n"
        for (var [k, v] of Object.entries(options)) {
          logtext += `@green!/${k}@!`
          for (var alias of v.alias ?? [])
            logtext += ` @green!/${alias}@!`
          for (var arg of v.args ?? []) {
            logtext += ` @blue!<@!@green!${arg[0]}${arg[1] ? `@!@blue!=@!@green!${arg[1]}` : ""}@!@blue!>@!`
          }
          logtext += `\n    ${v.desc}\n`
        }
        apLog(logtext.trimEnd())
      },
    },
    autoCloseDialogueBoxes: {
      desc: "don't wait for enter prompt on non battle end messages",
      args: [["on", "true/false"]],
      func(on) {
        localStorage.autoCloseDialogueBoxes = ["1", "true"].includes(
          on,
        )
      },
    },
    autoCloseBattleMessages: {
      desc: "don't wait for enter prompt on battle end messages",
      args: [["on", "true/false"]],
      func(on) {
        localStorage.autoCloseBattleMessages = ["1", "true"].includes(
          on,
        )
      },
    },
    instantBattleStarts: {
      desc: "encounters start instantly instead of waiting for the attacked text",
      args: [["on", "true/false"]],
      func(on) {
        localStorage.instantBattleStarts = ["1", "true"].includes(on)
        test.attackedTimer.__delay =
          localStorage.instantBattleStarts == "true" ? 0 : 1e3
      },
    },
    instantBattleEndText: {
      desc: "each line of loot text at battle end appears instantly",
      args: [["on", "true/false"]],
      func(on) {
        localStorage.instantBattleEndText = ["1", "true"].includes(on)
        test.batEndTimer.__delay =
          localStorage.instantBattleEndText == "true" ? 0 : 350
      },
    },
    debug: {
      desc: "enable debug/chear mode w/a/s/d moves one screen that dir\nrclick on game sets player tyo that position\ndbclick on map tps player to that screen",
      args: [["on", "true/false"]],
      func(on) {
        localStorage.debug = ["1", "true"].includes(on)
      },
    },
    owo: {
      desc: "enables owo mode",
      func() {
        owo = _owo
        localStorage.owo = true
      },
    },
    showPlayerPos: {
      desc: "toggle showing player position information in the bottom right of the game",
      func(on = true) {
        localStorage.showPlayerPos = ["1", "true"].includes(on)
      },
    },
    renderExits: {
      desc: "toggle showing each rooms exit regions ingame",
      func(on = true) {
        localStorage.renderExits = ["1", "true"].includes(on)
      },
    },
    renderCheckerboard: {
      desc: "toggle rendering a checkerboard over each tile ingame",
      func(on = true) {
        localStorage.renderCheckerboard = ["1", "true"].includes(on)
      },
    },
    showVanillaItems: {
      desc: "if enabled will always show the vanilla item and not the one that has been randomized to that spot",
      func(on = true) {
        localStorage.showVanillaItems = ["1", "true"].includes(on)
      },
    },
    reconnect: {
      desc: "reconnects to ap for if disconnected",
      func() {
        if (!window.ap) {
          apError(
            "ap not connected, use @green!/connect@! to connect for the first time",
          )
          return
        }
        ap.connect()
      },
    },
    runAPServer: {
      desc: "starts an ap server, pass seed to load old save",
      func(seed) {
        ArchipelagoClient.runAPServer(seed || undefined)
      },
    },
    time: {
      args: [["format", "12/24"]],
      desc: "changes time mode",
      func(format) {
        localStorage.timeFormat = format
      },
    },
    clear: {
      alias: ["c"],
      desc: "clears chat log",
      func(format) {
        window._apChatBuffer.forEach((e) => e.el.remove())
      },
    },
    nowo: {
      desc: "disables owo mode",
      func() {
        owo = nowo
        localStorage.owo = false
      },
    },
    connect: {
      desc: "connect to ap",
      args: [["host", "127.0.0.1:38281"], ["name"], ["password"]],
      func(host = "127.0.0.1:38281", name, password = "") {
        log(host, name, password)
        location.search = `?connect=${host}&name=${name}&password=${password}`
        if (window.playerLoaded && !window.ap) {
          location.reload()
        } else {
          apTryConnect()
        }
      },
    },
  }
  log(text)
  if (!text) return
  var [cmd, ...args] = (
    text.match(/[^\s"']+|"([^"]*)"|'([^']*)'/g) ?? [text]
  ).map((arg) => arg.replace(/^['"]|['"]$/g, ""))
  document.querySelector("#apChatSayInput").onblur?.()
  cmd = cmd.toLowerCase()
  for (var [k, v] of Object.entries(options)) {
    for (var kk of [...(v.alias ?? []), k]) {
      if (
        cmd == "/" + kk.toLowerCase() ||
        cmd == "/" + owo(kk).toLowerCase() ||
        owo(cmd) == "/" + kk.toLowerCase()
      ) {
        v.func(...args)
        input.value = ""
        return
      }
    }
  }
  if (!window.ap || !window.ap.isAuthenticated) {
    apWarn("Cannot send Say; not connected/authenticated yet.")
    return
  }
  window.ap.sendPackets([
    {
      cmd: "Say",
      text: text,
    },
  ])
  input.value = ""
}

document
  .getElementById("apChatSaySend")
  .addEventListener("click", apSendSayFromInput)

// 1. Keep track of history and where the user is currently looking
let history = []
let historyIndex = -1
let currentBuffer = "" // Stores what the user was typing before hitting 'Up'

document
  .getElementById("apChatSayInput")
  .addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      const text = this.value.trim()
      if (text) {
        if (history[history.length - 1] !== text) {
          history.push(text)
        }
        e.preventDefault()
        apSendSayFromInput()
      }

      // Reset navigation states for a fresh line
      historyIndex = -1
      currentBuffer = ""
      this.value = ""
    } else if (e.key === "ArrowUp") {
      // Prevent cursor from jumping to the beginning of the text box
      e.preventDefault()

      if (history.length === 0) return

      // If starting navigation, save what the user currently had typed
      if (historyIndex === -1) {
        currentBuffer = this.value
        historyIndex = history.length - 1
      } else if (historyIndex > 0) {
        historyIndex--
      }

      this.value = history[historyIndex]
    } else if (e.key === "ArrowDown") {
      e.preventDefault()

      if (historyIndex === -1) return

      if (historyIndex < history.length - 1) {
        historyIndex++
        this.value = history[historyIndex]
      } else {
        // Reached the bottom, restore what they were originally typing
        historyIndex = -1
        this.value = currentBuffer
      }
    }
  })

window.addEventListener("touchmove", function (event) {}, false)
if (
  typeof window.devicePixelRatio != "undefined" &&
  window.devicePixelRatio > 2
) {
  var meta = document.getElementById("viewport")
  meta.setAttribute(
    "content",
    "width=device-width, initial-scale=" +
      2 / window.devicePixelRatio +
      ", user-scalable=no",
  )
}
function toggleCollapse(on) {
  document
    .getElementById("apChatLogContainer")
    .classList.toggle("collapsed", on)
  document.getElementById("apChatLogToggle").textContent =
    (
      document
        .getElementById("apChatLogContainer")
        .classList.contains("collapsed")
    ) ?
      "▸"
    : "▾"
  localStorage.apLogVisible = !document
    .getElementById("apChatLogContainer")
    .classList.contains("collapsed")

  // Sync the toast fade state immediately so there's no one-frame
  // flash of every entry (collapsing) or of stale opacity/display
  // (expanding) before the interval next ticks.
  if (
    document
      .getElementById("apChatLogContainer")
      .classList.contains("collapsed")
  ) {
    window._apUpdateToastOpacities()
  } else {
    window._apResetEntryStyles()
  }
  window._apChatLogEl.scrollTop = window._apChatLogEl.scrollHeight
}
window.addEventListener(
  "keydown",
  function (e) {
    // Check for Tab key (9)
    if (e.keyCode === 9) {
      e.preventDefault() // Stop default browser focus switching

      var mapIframe = document.getElementById("map")
      if (mapIframe) {
        mapIframe.classList.toggle("in-front")
      }
    }

    // Existing space/arrow key protection
    if (
      [37, 38, 39, 40, 32, 8].indexOf(e.keyCode) > -1 &&
      document.activeElement?.nodeName != "INPUT" &&
      document.activeElement?.nodeName != "TEXTAREA"
    ) {
      e.preventDefault()
    }
    if (e.key == "`") {
      e.preventDefault()
      if (document.activeElement?.id != "apChatSayInput") {
        toggleCollapse(false)
        document.querySelector("#apChatSayInput").focus()
      } else {
        toggleCollapse(true)
      }
    }
    if (e.key == "/") {
      if (document.activeElement?.id != "apChatSayInput") {
        e.preventDefault()
        var col = document
          .getElementById("apChatLogContainer")
          .classList.contains("collapsed")
        if (col) {
          toggleCollapse(false)
        }
        document.querySelector("#apChatSayInput").focus()
        document.querySelector("#apChatSayInput").value = "/"
        if (col) {
          document.querySelector("#apChatSayInput").onblur = () => {
            document.querySelector("#apChatSayInput").onblur = null
            toggleCollapse(true)
          }
        }
      }
    }
    if (e.key == "Escape") {
      e.preventDefault()
      if (document.activeElement.id == "apChatSayInput") {
        document.activeElement.blur()
      }
    }
  },
  false,
)
