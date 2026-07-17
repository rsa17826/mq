#!/usr/bin/env python3
"""
Scans a file for instances of manager.quest[Enum.Quest...] followed by a comparison
operator (>, ==, <), shows the surrounding context, and interactively asks whether
to replace `manager.quest` with `questChecker` at that location.

Usage:
    python quest_replacer.py <path_to_file>

"""

import re
import sys
from pathlib import Path

# Matches "manager.quest" only when followed by "[Enum.Quest" and, somewhere after
# that, a comparison operator (>, ==, <).
PATTERN = re.compile(r"manager\.quest(?=\[Enum\.Quest)[^\n]*?(?:>|==|<)")

MARKER = "questChecker-reviewed" # comment text used to mark a line as already handled
CONTEXT_LINES = 20


def is_marked(lines, idx):
  """A line is considered already handled if the marker comment is present on it."""
  return MARKER in lines[idx]


def find_matches(text: str):
  """Yield (start, end, line_no) for each match, scanning line by line so we
  can report accurate line numbers and keep context extraction simple."""
  lines = text.splitlines(keepends=True)
  offset = 0
  matches = []
  for line_no, line in enumerate(lines, start=1):
    for m in PATTERN.finditer(line):
      matches.append((line_no, offset + m.start(), offset + m.end()))

    offset += len(line)

  return matches, lines


def show_context(lines, line_no):
  start = max(0, line_no - 1 - CONTEXT_LINES)
  end = min(len(lines), line_no + CONTEXT_LINES)
  print("-" * 60)
  for i in range(start, end):
    marker = ">>" if (i + 1) == line_no else "  "
    print(f"{marker} {i + 1:>5}: {lines[i].rstrip()}")

  print("-" * 60)


def main():
  if len(sys.argv) != 2:
    print("Usage: python quest_replacer.py <path_to_file>")
    sys.exit(1)

  path = Path(sys.argv[1])
  if not path.is_file():
    print(f"File not found: {path}")
    sys.exit(1)

  text = path.read_text(encoding="utf-8")
  matches, lines = find_matches(text)

  if not matches:
    print("No matches found.")
    return

  print(f"Found {len(matches)} match(es) in {path}\n")

  # We rebuild the file line-by-line, replacing "manager.quest" -> "questChecker"
  # only on lines the user confirms.
  changed = False
  for line_no, _, _ in matches:
    idx = line_no - 1
    line = lines[idx]

    # Re-check the line still matches (in case a prior replacement altered it)
    if not PATTERN.search(line):
      continue

    # Skip lines already reviewed/marked (comment at end of line, or alone on the line above)
    if is_marked(lines, idx):
      print(f"Line {line_no}: already marked, skipping.\n")
      continue

    show_context(lines, line_no)
    answer = input(f"Replace 'manager.quest' with 'questChecker' on line {line_no}? [y/N/q] ").strip().lower()

    if answer == "q":
      print("Quitting without further changes.")
      break

    if answer == "y":
      new_line = re.sub(r"manager\.quest(?=\[Enum\.Quest)", "questChecker", line)
    else:
      new_line = line

    # Mark the line either way, so a future run won't ask about it again.
    stripped = new_line.rstrip("\n")
    newline_char = new_line[len(stripped) :] or "\n"
    lines[idx] = f"{stripped}  // {MARKER}{newline_char}"

    changed = True
    print("Replaced and marked.\n" if answer == "y" else "Skipped and marked.\n")

  if changed:
    confirm = input(f"Save changes to {path}? [y/N] ").strip().lower()
    if confirm == "y":
      path.write_text("".join(lines), encoding="utf-8")
      print("Saved.")
    else:
      print("Discarded changes (file not modified).")
  else:
    print("No changes made.")


if __name__ == "__main__":
  main()
