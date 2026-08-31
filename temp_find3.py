import json

log_file = r"C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl"
with open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        if "all_settings_replacements.txt" in line:
            data = json.loads(line)
            if "tool_calls" in data:
                for tc in data["tool_calls"]:
                    if tc["name"] == "run_command" and "all_settings_replacements.txt" in tc["args"]["CommandLine"]:
                        print(tc["args"]["CommandLine"])
                        print("=====")
