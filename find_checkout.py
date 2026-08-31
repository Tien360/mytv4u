import json
for i, line in enumerate(open(r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8')):
    if 'git checkout lib/screens/settings_screen.dart' in line:
        print(f"Git checkout at line {i}")
