import json
import ollama
import os
import subprocess

def open_in_codium(file_path, line_number):
    return
    """
    Opens VSCodium and focuses on the specified line number.
    """
    abs_path = os.path.abspath(file_path)
    target = f"{abs_path}:{line_number}"
    try:
        subprocess.run(["codium", "--goto", target], check=True)
        print(f"Successfully opened Codium at line {line_number}")
    except FileNotFoundError:
        print("Error: 'codium' command not found in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to launch Codium: {e}")

def extract_code_snippets_by_gaps(file_path, metadata, max_gap=50):
    """
    Groups line numbers into clusters if they are close.
    If gaps are large, treats them as separate segments.
    If only one line number exists total, pads it 5 lines up and 20 lines down.
    """
    items_with_lines = []
    for category in ["comparisons", "assignments"]:
        for item in metadata.get(category, []):
            if "line" in item:
                items_with_lines.append((int(item["line"]), category, item))

    if not items_with_lines:
        print("No line numbers found in metadata to grab code.")
        return []

    items_with_lines.sort(key=lambda x: x[0])

    clusters = []
    current_cluster = [items_with_lines[0]]

    for next_item in items_with_lines[1:]:
        if next_item[0] - current_cluster[-1][0] <= max_gap:
            current_cluster.append(next_item)
        else:
            clusters.append(current_cluster)
            current_cluster = [next_item]
    clusters.append(current_cluster)

    snippets_to_process = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Could not find the file at {file_path}")
        return []

    for idx, cluster in enumerate(clusters):
        cluster_lines = [x[0] for x in cluster]
        min_ln = min(cluster_lines)
        max_ln = max(cluster_lines)

        if idx == 0:
            open_in_codium(file_path=file_path, line_number=min_ln)

        if len(cluster_lines) == 1:
            start_line = max(1, min_ln - 5)
            end_line = min(len(all_lines), min_ln + 20)
        else:
            start_line = max(1, min_ln - 5)
            end_line = min(len(all_lines), max_ln + 5)

        snippet_text = "".join(all_lines[start_line - 1 : end_line])

        sub_metadata = {
            "north": metadata.get("north"),
            "east": metadata.get("east"),
            "comparisons": [item for ln, cat, item in cluster if cat == "comparisons"],
            "assignments": [item for ln, cat, item in cluster if cat == "assignments"]
        }

        snippets_to_process.append({
            "code_snippet": snippet_text,
            "sub_metadata": sub_metadata,
            "start_line": start_line # Stored here to trace back without LLM guessing
        })

    return snippets_to_process

def convert_logic_to_map_format(file_path, parsed_json_snippet):
    segments = extract_code_snippets_by_gaps(file_path, parsed_json_snippet)
    if not segments:
        return None

    system_prompt = (
        "You are an accurate data conversion assistant. Your job is to read raw code snippets "
        "and metadata, extract the logical requirements, and output a valid JSON array matching the target format. "
        "Do not include conversational text, markdown formatting blocks (like ```json), or explanations. Output ONLY valid raw JSON."
    )

    # Reverted Few-shot back to your original format without demanding "line" work from LLM
    few_shot_prompt = """
Example Input:
Code Snippet:
```
manager.quest[manager.pam]++
manager.blueFlower.set_visible(False)
} else if (
((manager.north == 3 &&
(manager.east == 20 || manager.east == 19)) ||
(manager.north == 4 && manager.east == 19)) &&
manager.inWater == 0 &&
manager.quest[manager.isles] == 3 &&
V.digVar >= 75
) {
manager.mess.set_text("You found a Terra Geode!")
manager.quest[manager.isles] = 4
} else if (
manager.north == 21 &&
manager.east == 23 &&
```
Metadata JSON:
```
{
"north": 4,
"east": 19,
"comparisons": [
{ "name": "isles", "value": "3", "line": 53528 }
],
"assignments": [
{ "name": "isles", "value": "4", "line": 53532 }
]
}
```

Example Output:
```
[
  {
    "room": { "north": 3, "east": 20 },
    "requires": [["quest:isles#3"]],
    "receive": ["quest:isles#4"]
  },
  {
    "room": { "north": 3, "east": 19 },
    "requires": [["quest:isles#3"]],
    "receive": ["quest:isles#4"]
  },
  {
    "room": { "north": 4, "east": 19 },
    "requires": [["quest:isles#3"]],
    "receive": ["quest:isles#4"]
  }
]
```
Now process the following input. Follow the pattern precisely.
"""

    combined_results = []

    for seg in segments:
        print(f"--- Processing code snippet window (Starting line {seg['start_line']}) ---\n")
        print(seg['code_snippet'])
        user_content = f"""
Code Snippet:
{seg['code_snippet']}

Metadata JSON:
{json.dumps(seg['sub_metadata'], indent=2)}

Output:
"""

        response = ollama.generate(
            model='qwen2.5-coder:3b',
            system=system_prompt,
            prompt=few_shot_prompt + user_content,
            options={"temperature": 0.0}
        )

        raw_output = response['response'].strip()

        if raw_output.startswith("```"):
            raw_output = raw_output.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
            if raw_output.startswith("json"):
                raw_output = raw_output.split("\n", 1)[1].strip()

        try:
            segment_json = json.loads(raw_output)

            # --- Python Post-Processing Injection ---
            # Automatically track and add the context start line to the results
            if isinstance(segment_json, list):
                for item in segment_json:
                    if isinstance(item, dict):
                        item["line"] = seg["start_line"]
                combined_results.extend(segment_json)
            elif isinstance(segment_json, dict):
                segment_json["line"] = seg["start_line"]
                combined_results.append(segment_json)

        except json.JSONDecodeError:
            print("Failed to parse LLM segment output as JSON. Raw response:")
            print(raw_output)

    return combined_results

# --- Execution ---
if __name__ == "__main__":
    file_path = "MathQuest/MathQuest.js"
    with open("./quests.json") as ff:
      for current_metadata in json.load(ff):
        result = convert_logic_to_map_format(file_path, current_metadata)

        if result:
            progression_path = "./json/progression.json"
            if os.path.exists(progression_path):
                with open(progression_path, "r+", encoding='utf-8') as f:
                    data = json.load(f)
                    if 'locations' not in data:
                        data['locations'] = []
                    data['locations'].extend(result)
                    f.seek(0)
                    json.dump(data, f, indent=2)
                    f.truncate()
            else:
                print(f"Could not find baseline path: {progression_path}. Printing output instead:")

        print(json.dumps(result, indent=2))