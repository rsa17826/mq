// Reachability / logic engine.
// Requires PROG_DATA (prog.js), AP_ITEM_IDS (game globals), and tracker.js's
// data-location markers to already be present on the page.

(function () {
  function init() {
    if (typeof PROG_DATA === "undefined" || typeof AP_ITEM_IDS === "undefined" || !window.ap) {
      setTimeout(init, 250);
      return;
    }

    // Ground truth for "is this token a real network item" (vs a free/virtual
    // flag like area:/quest:, or an unresolvable entrance.* token).
    const REAL_ITEM_NAMES = new Set(Object.values(AP_ITEM_IDS));

    function isEntranceToken(tok) {
      return tok.startsWith("entrance.");
    }

    // Cache icon elements by their "room - item" location key.
    const iconsByLocation = {};
    document.querySelectorAll(".progression-icon[data-location]").forEach((el) => {
      (iconsByLocation[el.dataset.location] ||= []).push(el);
    });

    const haveReal = new Set(); // real items actually received over the network

    // Evaluate one AND-group: 'true' (satisfied), 'false' (missing something
    // real), or 'unknown' (would be satisfied but gated behind a specific
    // room entrance/route we can't verify).
    function evalGroup(group, have) {
      if (group.length === 0) return "true";
      let hasEntrance = false;
      for (const tok of group) {
        if (isEntranceToken(tok)) {
          hasEntrance = true;
          continue;
        }
        if (!have.has(tok)) return "false";
      }
      return hasEntrance ? "unknown" : "true";
    }

    // Evaluate an entry: best result across its OR-groups.
    function evalEntry(entry, have) {
      let best = "false";
      for (const group of entry.requires || []) {
        const r = evalGroup(group, have);
        if (r === "true") return "true";
        if (r === "unknown") best = "unknown";
      }
      return best;
    }

    function recompute() {
      const have = new Set(haveReal);
      const status = new Array(PROG_DATA.length).fill("false");
      let changed = true;

      while (changed) {
        changed = false;
        for (let i = 0; i < PROG_DATA.length; i++) {
          if (status[i] === "true") continue; // already fully resolved
          const entry = PROG_DATA[i];
          const r = evalEntry(entry, have);
          status[i] = r;
          if (r === "true") {
            for (const tok of entry.receive) {
              // only virtual/free tokens auto-propagate; real items only
              // enter `have` via actual ReceivedItems packets
              if (!REAL_ITEM_NAMES.has(tok) && !have.has(tok)) {
                have.add(tok);
                changed = true;
              }
            }
          }
        }
      }

      // Clear old logic markers, but never touch .checked (that's ground truth)
      document
        .querySelectorAll(".progression-icon.in-logic, .progression-icon.route-unknown")
        .forEach((el) => el.classList.remove("in-logic", "route-unknown"));

      PROG_DATA.forEach((entry, i) => {
        const r = status[i];
        if (r === "false") return;
        for (const tok of entry.receive) {
          if (!REAL_ITEM_NAMES.has(tok)) continue; // virtual flag, no map marker
          const key = `${entry.room} - ${tok}`;
          const els = iconsByLocation[key];
          if (!els) continue;
          els.forEach((el) => {
            if (el.classList.contains("checked")) return; // already collected, leave alone
            el.classList.add(r === "true" ? "in-logic" : "route-unknown");
          });
        }
      });
    }

    const origOnReceivedItems = ap.onReceivedItems.bind(ap);
    ap.onReceivedItems = function (packet) {
      origOnReceivedItems(packet);
      packet.items.forEach((item) => {
        const name = AP_ITEM_IDS[item.item];
        if (name) haveReal.add(name);
      });
      recompute();
    };

    const origOnConnected = ap.onConnected.bind(ap);
    ap.onConnected = function (packet) {
      origOnConnected(packet);
      recompute();
    };

    recompute();
    console.log(`[logic] reachability engine ready: ${PROG_DATA.length} entries`);
  }

  init();
})();
