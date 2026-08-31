import json
with open('line32375.txt', 'w', encoding='utf-8') as f:
    for i, line in enumerate(open(r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8')):
        if i == 32374: # 32375 is index 32374 probably? Or index i?
            obj = json.loads(line)
            if 'content' in obj:
                f.write(obj['content'])
            break
