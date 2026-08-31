import json
import codecs

log_file = r"C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl"
last_settings = None

with codecs.open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except:
            continue
        if "tool_calls" in data:
            for tc in data["tool_calls"]:
                if tc["name"] == "write_to_file" and tc["args"].get("TargetFile", "").endswith("settings_screen.dart"):
                    last_settings = tc["args"]["CodeContent"]
                
                # Check run_command for anything that echoes or overwrites it entirely
                if tc["name"] == "run_command":
                    cmd = tc["args"].get("CommandLine", "")
                    if "Set-Content" in cmd and "settings_screen.dart" in cmd:
                        pass # too hard to parse

print(f"Found a write_to_file? {'Yes' if last_settings else 'No'}")
if last_settings:
    with codecs.open("settings_screen_backup.dart", "w", encoding="utf-8") as out:
        out.write(last_settings)
