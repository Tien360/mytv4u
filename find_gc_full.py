import json

for i, line in enumerate(open(r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8')):
    if i in [32097, 32099, 32209]:
        obj = json.loads(line)
        for tc in obj.get('tool_calls', []):
            args = tc.get('args', {})
            print(f"--- Line {i} ---\n{args.get('CommandLine', '')}\n")
