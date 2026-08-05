// =====================================================================
// SAVE FILE SELECTOR
//
// A simple DOM-based panel, shown whenever window.saveFileSelectorVisible
// is truthy, listing every save in window.saveData (skipping the special
// "nonAP" entry, which isn't a real per-connection save). Each row shows
// the save's key and -- if it has AP connection info attached -- lets the
// player reconnect to that exact server/slot with one click, the same way
// the /connect chat command does. A delete button removes that save
// entirely from window.saveData.
// =====================================================================
class SaveFileSelector {
  /**@type {HTMLElement} */
  static panel
  /**@type {HTMLElement} */
  static list

  static _buildUi() {
    SaveFileSelector.panel = newelem(
      "div",
      {
        id: "save-file-selector-panel",
        position: "fixed",
        top: "0",
        left: "0",
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "rgba(0,0,0,0.75)",
        zIndex: "20000000",
        fontFamily: "monospace",
        color: "#e0e0e0",
      },
      [
        newelem(
          "div",
          {
            background: "rgba(20,20,20,0.98)",
            border: "1px solid #444",
            borderRadius: "8px",
            padding: "16px",
            minWidth: "360px",
            maxWidth: "90vw",
            maxHeight: "80vh",
            overflowY: "auto",
          },
          [
            newelem(
              "div",
              {
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "10px",
              },
              [
                newelem("b", { fontSize: "16px" }, ["Select Save"]),
                newelem(
                  "button",
                  {
                    onclick: () => {
                      SaveFileSelector.hide()
                    },
                  },
                  ["✕"],
                ),
              ],
            ),
            (SaveFileSelector.list = newelem("div", {
              id: "save-file-selector-list",
              display: "flex",
              flexDirection: "column",
              gap: "6px",
            })),
          ],
        ),
      ],
    )
    document.body.appendChild(SaveFileSelector.panel)
  }

  static buildRow(key) {
    const data = window.saveData[key]
    const ap = data && data.ap

    return newelem(
      "div",
      {
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: "10px",
        background: "rgba(255,255,255,0.05)",
        border: "1px solid #333",
        borderRadius: "6px",
        padding: "8px 10px",
      },
      [
        newelem("div", { display: "flex", flexDirection: "column" }, [
          newelem("div", { fontWeight: "bold" }, [key]),
          ap ?
            newelem("div", { fontSize: "12px", color: "#aaa" }, [
              `${ap.playerName}@${ap.hostname}${ap.port ? `:${ap.port}` : ""} (${ap.game})`,
            ])
          : newelem("div", { fontSize: "12px", color: "#888" }, [
              "(no AP connection info)",
            ]),
        ]),
        newelem("div", { display: "flex", gap: "6px" }, [
          ap ?
            newelem(
              "button",
              {
                title: "Connect to this save's server",
                onclick: (e) => {
                  e.stopPropagation()
                  SaveFileSelector.hide()
                  location.search = `?connect=${ap.hostname}${ap.port ? `:${ap.port}` : ""}&name=${encodeURIComponent(ap.playerName)}&password=${encodeURIComponent(ap.password || "")}`
                  if (window.playerLoaded && !window.ap) {
                    location.reload()
                  } else {
                    apTryConnect()
                  }
                },
              },
              ["Connect"],
            )
          : null,
          newelem(
            "button",
            {
              title: "Delete this save",
              onclick: (e) => {
                e.stopPropagation()
                if (
                  !confirm(
                    `Delete save "${key}"? This cannot be undone.`,
                  )
                )
                  return
                delete window.saveData[key]
                SaveFileSelector.render()
              },
            },
            ["Delete"],
          ),
        ]),
      ],
    )
  }

  static render() {
    if (!SaveFileSelector.list) return
    SaveFileSelector.list.innerHTML = ""
    const keys = Object.keys(window.saveData || {}).filter(
      (k) => k !== "nonAP",
    )
    if (!keys.length) {
      SaveFileSelector.list.appendChild(
        newelem("div", { color: "#888" }, ["No saves found."]),
      )
      return
    }
    keys.forEach((key) => {
      SaveFileSelector.list.appendChild(
        SaveFileSelector.buildRow(key),
      )
    })
  }

  static show() {
    if (!SaveFileSelector.panel) SaveFileSelector._buildUi()
    SaveFileSelector.panel.style.display = "flex"
    SaveFileSelector.render()
  }
  static hide() {
    if (!SaveFileSelector.panel) SaveFileSelector._buildUi()
    SaveFileSelector.panel.style.display = "none"
  }
}
