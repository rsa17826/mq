import re
import json

file_path = "MathQuest/MathQuest.base.js"

with open(file_path, "r") as f:
    lines = f.readlines()

json_output = []

def parse_numeric_value(value_str):
    """Converts JavaScript numeric or scientific notation strings safely into integers."""
    if 'e' in value_str.lower():
        return int(float(value_str))
    return int(value_str)

for i, line in enumerate(lines):
    if "newItem(" in line:
        item_match = re.search(r'newItem\(\s*["\']([^"\']+)["\']\s*\)', line)
        if not item_match:
            continue

        item_raw = item_match.group(1)
        coords_match = re.match(r"(\d+)_(\d+)", item_raw)

        # If room coordinates exist in the string use them, otherwise default to 0
        file_north, file_east = (int(coords_match.group(1)), int(coords_match.group(2))) if coords_match else (0, 0)
        receive_item = item_raw.split(" - ")[-1] if " - " in item_raw else item_raw

        # --- DYNAMIC BOUNDARY DETECTION ---
        # Scan backward up to 30 lines to find exactly where this conditional statement block starts
        start_idx = i
        for j in range(i - 1, max(-1, i - 30), -1):
            if "if (" in lines[j] or "if(" in lines[j]:
                start_idx = j
                # If the line right above this block also has item setups, keep it,
                # but breaking here isolates the conditional statement perfectly.
                break

        block_context = "".join(lines[start_idx:i+1])
        cleaned_context = block_context.replace(" ", "")

        requires = []

        # 1. Room Coordinate Override (Prioritize direct manager.north / manager.east checks inside the block)
        north_match = re.search(r"manager\.north==(\d+)", cleaned_context)
        east_match = re.search(r"manager\.east==(\d+)", cleaned_context)

        final_north = int(north_match.group(1)) if north_match else file_north
        final_east = int(east_match.group(1)) if east_match else file_east

        # 2. Base Currencies (Gold, Medallions, Rubies, Slamstones, ShadowCrests)
        currencies = ["gold", "medallions", "rubies", "slamstones", "shadowCrest"]
        for cur in currencies:
            gte = re.search(fr"manager\.{cur}>=([\d\.e\+]+)", cleaned_context)
            gt = re.search(fr"manager\.{cur}>([\d\.e\+]+)", cleaned_context)
            eq = re.search(fr"manager\.{cur}==([\d\.e\+]+)", cleaned_context)

            if gte:
                requires.append(f"{cur}:{parse_numeric_value(gte.group(1))}")
            elif gt:
                requires.append(f"{cur}:{parse_numeric_value(gt.group(1)) + 1}")
            elif eq:
                requires.append(f"{cur}:{parse_numeric_value(eq.group(1))}")

        if "--manager.gold" in cleaned_context:
            requires.append("gold:1")

        # 3. Loot Table Requirements (e.g., manager.loot[Enum.Loot.gFeather] >= 3)
        loot_matches = re.findall(r"manager\.loot\[Enum\.Loot\.(\w+)\]>=(\d+)", block_context.replace(" ", ""))
        for loot_name, loot_qty in loot_matches:
            requires.append(f"loot:{loot_name}:{loot_qty}")

        # 4. Skill Level Progression (e.g., manager.skills[Enum.Skill.medic] == 5)
        skill_lvls = re.findall(r"manager\.skills\[Enum\.Skill\.(\w+)\]==(\d+)", block_context.replace(" ", ""))
        for skill, lvl in skill_lvls:
            if lvl == "0":
                requires.append(f"no_skill:{skill}")
            else:
                requires.append(f"skill:{skill}:level_{lvl}")

        # Fallback to general skill presence if absolute level equality wasn't found
        if not skill_lvls:
            skill_matches = re.findall(r"Enum\.Skill\.(\w+)", block_context)
            for skill in skill_matches:
                if f"manager.skills[Enum.Skill.{skill}]==0" in cleaned_context:
                    requires.append(f"no_skill:{skill}")
                elif f"manager.skills[Enum.Skill.{skill}]" in cleaned_context:
                    requires.append(f"skill:{skill}")

        # 5. Magic Systems
        magic_matches = re.findall(r"Enum\.Magic\.(\w+)", block_context)
        for magic in magic_matches:
            if f"manager.magic[Enum.Magic.{magic}]<1" in cleaned_context or f"manager.magic[Enum.Magic.{magic}]==0" in cleaned_context:
                requires.append(f"no_magic:{magic}")

        # 6. Weapon Systems
        weap_matches = re.findall(r"Enum\.Weapon\.(\w+)", block_context)
        for weap in weap_matches:
            if f"manager.weapon[Enum.Weapon.{weap}]<1" in cleaned_context or f"manager.weapon[Enum.Weapon.{weap}]==0" in cleaned_context:
                requires.append(f"no_weapon:{weap}")

        # 7. Food Space Systems
        food_matches = re.findall(r"Enum\.Food\.(\w+)", block_context)
        for food in food_matches:
            requires.append(f"food_space:{food}")

        # Clean duplicates while preserving sequence order
        seen = set()
        unique_requires = [x for x in requires if not (x in seen or seen.add(x))]

        json_output.append({
            "room": {"north": final_north, "east": final_east},
            "requires": [unique_requires],
            "receive": [receive_item]
        })

print(f"Successfully processed {len(json_output)} items.")

with open("items.json", "w") as out_file:
    json.dump(json_output, out_file, indent=4)