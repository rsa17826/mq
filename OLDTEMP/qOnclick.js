onclick = () => {
  window.selectedThing = [
    ...Object.entries(manager)
      .filter(
        ([k, e]) =>
          !["whiteFlash"].includes(k) &&
          e?.get_visible?.() &&
          e?.hitTestPoint?.(
            test.get_mouseX(),
            test.get_mouseY(),
            true,
          ),
      )
      .map((e) => e[0]),
    ...Object.entries(manager)
      .filter(
        ([k, e]) =>
          !["sand", "grass"].includes(k) &&
          !k.includes("Floor") &&
          !k.includes("floor"),
      )
      .map(([k, e]) =>
        e
          ?.map?.((e, i) =>
            (
              e?.get_visible?.() &&
              e?.hitTestPoint?.(
                test.get_mouseX(),
                test.get_mouseY(),
                true,
              )
            ) ?
              [k, i]
            : null,
          )
          .filter(Boolean),
      )
      .filter((e) => e?.length)
      .map((e) => e[0].join("|")),
  ].join("\n")
  navigator.clipboard.writeText(window.selectedThing)
  log(window.selectedThing)
}
