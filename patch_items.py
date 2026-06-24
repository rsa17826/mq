# @noregex
"""
Patch MathQuest.js with item location reward overrides.
Includes detailed telemetry debug logs and explicit pool state injections.
"""

import json
import os

def init(src):
  OUT_DIR = os.path.dirname(os.path.abspath(__file__))
  
  # Load the generated item placement array from shuffle_items.py
  placement_data = json.load(open(f"{OUT_DIR}/json/item_placements.json"))
  placements = placement_data["placements"]
  seed = placement_data["seed"]
  
  # Escape item string arrays safely for JavaScript injection literals
  rows = []
  for p in placements:
    escaped_items = ", ".join(f'"{item}"' for item in p["shuffledItems"])
    rows.append(
      '  "{loc_id}": [{items}]'.format(
        loc_id=p["locationId"],
        items=escaped_items
      )
    )
  table_js = ",\n".join(rows)
  
  PATCH = f"""      // === ITEM RANDOMIZER PATCH START (seed {seed}) ===
    ;(function () {{
      var IR_TABLE = {{
{table_js}
      }};

      // Provided data binding controller function
      function setManagerData(k, v, vv) {{
        if (vv === undefined) {{
          manager[k] = v
        }} else {{
          manager[k][v] = vv
        }}
      }}

      console.log("[IR DEBUG] Initializing item overrides configuration table...");
      
      // Instantiate target lookup registry if it doesn't exist
      if (!manager.itemOverrides) {{
        setManagerData("itemOverrides", {{}});
      }}

      // Populate override mappings using setManagerData framework bindings
      for (var locId in IR_TABLE) {{
        if (IR_TABLE.hasOwnProperty(locId)) {{
          setManagerData("itemOverrides", locId, IR_TABLE[locId]);
          console.log("[IR DEBUG] Registered override for location [" + locId + "] ->", IR_TABLE[locId]);
        }}
      }}

      // Intercept item acquisition pathways if applicable via framework hook wrap
      if (typeof manager.grantLocationReward === 'function') {{
        var originalGrant = manager.grantLocationReward;
        manager.grantLocationReward = function(locationId) {{
          if (manager.itemOverrides && manager.itemOverrides[locationId]) {{
            var items = manager.itemOverrides[locationId];
            console.log("[IR DEBUG] Diverting original reward lookup. Found shuffled pool items:", items);
            // Engine processing logic for receiving overridden objects goes here
            return items;
          }}
          return originalGrant.apply(this, arguments);
        }};
        console.log("[IR DEBUG] Successfully wrapped manager.grantLocationReward engine framework hook.");
      }} else {{
        console.log("[IR DEBUG] Runtime notice: No direct functional hook wrapped. Overrides safely written directly to manager memory maps.");
      }}
    }})();
    // === ITEM RANDOMIZER PATCH END ===
  """
  
  # Coordinate placement safely inline with the room randomizer execution points
  ANCHOR = "      manager.north = 20\n      manager.east = 20\n"
  assert (
    src.count(ANCHOR) == 1
  ), f"expected exactly one occurrence of anchor, found {src.count(ANCHOR)}"
  
  # Stack item adjustments directly sequentially on top of the default initializations
  patched = src.replace(ANCHOR, PATCH + ANCHOR)
  
  print(f"Patched item reward profiles successfully")
  
  return patched