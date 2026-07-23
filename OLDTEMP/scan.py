import re
from collections import defaultdict

path = "./MathQuest/MathQuest.js"
with open(path, encoding="utf-8") as f:
    text = f.read()

coord_re = re.compile(r'manager\.north\s*==\s*(\d+)\s*&&\s*manager\.east\s*==\s*(\d+)')
matches = list(coord_re.finditer(text))

def line_no(pos):
    return text.count('\n', 0, pos) + 1

def extract_block(pos):
    brace_start = text.find('{', pos)
    if brace_start == -1:
        return ""
    depth = 0
    i = brace_start
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[brace_start:i+1]
        i += 1
    return text[brace_start:]

results = []
for i, m in enumerate(matches):
    coord = (m.group(1), m.group(2))
    block = extract_block(m.end())

    tbox_used = re.findall(r'tBoxUsed\[(\d+)\]', block)
    coord_strings = re.findall(r'"(\d+_\d+)\s*-', block)

    results.append({
        "line": line_no(m.start()),
        "coord": coord,
        "tBoxUsed": tbox_used,
        "coord_strings": set(coord_strings),
    })

by_coord = defaultdict(list)
for r in results:
    by_coord[r["coord"]].append(r)

print(f"Total coordinate-check blocks found: {len(results)}")
print(f"Unique coordinates: {len(by_coord)}\n")

mismatches = []
for coord, entries in by_coord.items():
    all_tbox = set()
    for e in entries:
        all_tbox.update(e["tBoxUsed"])
    if len(all_tbox) > 1:
        mismatches.append((coord, entries, all_tbox))

print(f"=== Coordinates with INCONSISTENT tBoxUsed values: {len(mismatches)} ===\n")
for coord, entries, all_tbox in mismatches:
    print(f"Coord north={coord[0]} east={coord[1]}  -> tBoxUsed values found: {sorted(all_tbox)}")
    for e in entries:
        print(f"   line {e['line']}: tBoxUsed={e['tBoxUsed']}  coord_strings={e['coord_strings']}")
    print()

print("\n=== Coordinates where tBoxUsed index doesn't match expected 'north_east' string pattern (sanity check) ===")
for r in results:
    n, e_ = r["coord"]
    expected_str = f"{n}_{e_}"
    if r["coord_strings"] and expected_str not in r["coord_strings"]:
        print(f"line {r['line']}: coord={r['coord']} tBoxUsed={r['tBoxUsed']} strings_found={r['coord_strings']} (expected {expected_str})")
