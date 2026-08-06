#!/usr/bin/env python3
"""
Patch MathQuest.js's embedded Lime/OpenFL asset manifest to register
additional image assets (e.g. img/test.png) that exist on disk but
weren't part of the original compiled manifest.

Usage:
    python3 patch_manifest.py <path-to-MathQuest.js> <img-dir> <asset1.png> [asset2.png ...]

Example:
    python3 patch_manifest.py MathQuest.js img test.png

This will look for MathQuest/img/test.png relative to <img-dir>, read its
byte size, build a properly-formatted manifest record, and splice it into
the big asset library manifest (the one containing img%2F... entries),
right before the FONT/MUSIC entries begin.

The script edits a COPY (writes to <input>.patched.js) so the original is
never touched.
"""
import sys
import os
import re

def build_entry(rel_path_url_encoded, size_bytes):
    """Build a Haxe-serializer 'o' (object) record in fully spelled-out form.
    Format matches: o "path" <path> "size" <int> "type" "IMAGE" "id" <path> "preload" true g
    """
    def s(field):
        return f"y{len(field)}:{field}"

    path_field = rel_path_url_encoded
    id_field = rel_path_url_encoded

    # Insertion point sits right after the "g" that already closed the
    # PREVIOUS entry's object, so we only need to OPEN a new object here
    # ("o"), not close anything from before. Our own object is closed with
    # a trailing "g", and the ORIGINAL content that follows (starting with
    # "o" for the FONT entry) opens the next object as normal.
    entry = (
        "o"
        + s("path") + s(path_field)
        + s("size") + f"i{size_bytes}"
        + s("type") + s("IMAGE")
        + s("id") + s(id_field)
        + s("preload") + "t"
        + "g"
    )
    return entry


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    js_path = sys.argv[1]
    img_dir = sys.argv[2]
    assets = sys.argv[3:]

    with open(js_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the SECOND manifest blob (the big one with img%2F... assets).
    # We locate it by searching for the distinctive marker used inside it.
    marker = 'img%2Farmor%2FalphaArmorTile.png'
    idx = content.find(marker)
    if idx == -1:
        print("ERROR: could not find the main asset manifest blob (marker not found).")
        sys.exit(1)

    # Within that blob, find where image entries end and FONT entries begin.
    # Font entries are marked by the literal 'y4:FONT' after image entries finish,
    # preceded by a length-prefixed 'R2i<bytes>R3' back-reference chain.
    # We anchor on the first occurrence of 'y4:FONT' AFTER idx.
    font_idx = content.find("y4:FONT", idx)
    if font_idx == -1:
        print("ERROR: could not find the FONT section boundary in the manifest.")
        sys.exit(1)

    # Walk backwards from font_idx to the nearest preceding 'R6t' which closes
    # the last image record (pattern: ...R6tgoR0y...pngR2i<size>R3R4R5R###R6t)
    # then continue backward to find where the *next* token starts (R2i...R3 ref
    # chain feeding into FONT). We insert right after the last 'R6t' that
    # belongs to an image record and before that trailing ref chain.
    search_region = content[idx:font_idx]
    # Anchor on "R6tg": R6t closes the preceding entry's preload=true field,
    # and the immediately following "g" closes that entry's object. We must
    # insert AFTER that "g" (not before it), otherwise we split the prior
    # entry's own close-token away from it and end up with a duplicate "g"
    # in the stream, which breaks the Haxe unserializer ("Invalid char g").
    anchor = "R6tg"
    last_anchor = search_region.rfind(anchor)
    if last_anchor == -1:
        print("ERROR: could not find insertion anchor (R6tg) before FONT section.")
        sys.exit(1)

    insertion_point = idx + last_anchor + len(anchor)

    # Build new entries for each requested asset
    new_entries = []
    for asset in assets:
        # locate file on disk to get real byte size
        candidates = [
            os.path.join(img_dir, asset),
            os.path.join(img_dir, "img", asset),
        ]
        file_path = None
        for c in candidates:
            if os.path.isfile(c):
                file_path = c
                break
        if file_path is None:
            print(f"WARNING: could not find '{asset}' under '{img_dir}' — skipping. "
                  f"(tried: {candidates})")
            continue

        size_bytes = os.path.getsize(file_path)
        rel = f"img/{asset}".replace("/", "%2F")
        entry = build_entry(rel, size_bytes)
        new_entries.append(entry)
        print(f"Prepared entry for img/{asset}: {size_bytes} bytes")

    if not new_entries:
        print("No entries were added. Aborting without writing output.")
        sys.exit(1)

    patched = (
        content[:insertion_point]
        + "".join(new_entries)
        + content[insertion_point:]
    )

    out_path = os.path.splitext(js_path)[0] + ".patched.js"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(patched)

    print(f"\nDone. Patched file written to: {out_path}")
    print(f"Inserted {len(new_entries)} entr{'y' if len(new_entries)==1 else 'ies'} "
          f"at byte offset {insertion_point}.")


if __name__ == "__main__":
    main()
