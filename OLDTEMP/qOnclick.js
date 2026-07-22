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

function removeDuplicates(obj) {
  for (const key in obj) {
    if (Array.isArray(obj[key])) {
      // Deduplicate the array using Set
      obj[key] = [...new Set(obj[key])]
    } else if (typeof obj[key] === "object" && obj[key] !== null) {
      // Recurse into nested objects
      removeDuplicates(obj[key])
    }
  }
  return obj
}

// Clean window.q in-place
removeDuplicates(window.q)
