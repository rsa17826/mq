# Define which exits connect to which physical island/zone inside room (11, 20)
room_exit_zones = {
  "west0": "ZoneA",
  "south0": "ZoneA",

  "north0": "ZoneB", # Stepping-stone middle spot

  "south1": "ZoneC",
  "east0": "ZoneC",
  "north1": "ZoneC"
}

import json

# Configuration for room (11, 20)
NORTH = 11
EAST = 20

# Define which exits belong to the same reachable sub-sections
exit_zones = {
  "south0": "zone_left",
  "west0": "zone_left",

  "south1": "zone_right",
  "east0": "zone_right",
  "north0": "zone_right"
}

gates = []
exits = list(exit_zones.keys())

# Permute combinations automatically
for i in range(len(exits)):
  for j in range(i + 1, len(exits)):
    exit_a = exits[i]
    exit_b = exits[j]

    # If they are in the same zone, they can reach each other!
    if exit_zones[exit_a] == exit_zones[exit_b]:
      gate_entry = {
        "room": { "north": NORTH, "east": EAST },
        "from": exit_a,
        "to": exit_b,
        "bidirectional": True,
        "requires": [[]] # Empty array means open, fill with requirements if locked
      }
      gates.append(gate_entry)

# Print out your final formatted text block
print(json.dumps(gates, indent=2))