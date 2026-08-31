import json
for line in open(r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8'):
    if '_audioKey' in line and 'lib/screens/settings_screen.dart' in line:
        print(len(line))
        # Let's extract the exact ReplacementContent or CodeContent!
