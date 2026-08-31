import json
with open('line9523.txt', 'w', encoding='utf-8') as f:
    for i, line in enumerate(open(r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8')):
        if i in [9523, 9522]:
            obj = json.loads(line)
            f.write(json.dumps(obj, indent=2))
            f.write('\n')
