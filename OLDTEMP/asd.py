from _room_geometry import GEOM, ExitBase


def find_unsorted_exits(rooms: ExitBase):
  for idx, room in enumerate(rooms):
    pos_str = f"Room {idx} (north: {room.get('north')}, east: {room.get('east')})"
    exits = room.get("exits", {})

    for direction, segments in exits.items():
      # Skip empty exit lists
      if not segments or len(segments) <= 1:
        continue

      # Identify the primary sorting key dynamically ('top' or 'left')
      # If 'top' is in the dict, we use 'top', otherwise we fallback to 'left'
      sort_key = "top" if "top" in segments[0] else "left"

      # Extract the values to see if they are strictly ascending
      values = [seg[sort_key] for seg in segments]

      # Check if the list is sorted in ascending order
      is_sorted = all(values[i] <= values[i + 1] for i in range(len(values) - 1))

      if not is_sorted:
        print(f"⚠️ {pos_str} has unsorted exits in direction '{direction}'!")
        print(f"   Current order of `{sort_key}`: {values}\n")


# Run the check
find_unsorted_exits(GEOM)
