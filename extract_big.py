import json
with open('big_contents.txt', 'w', encoding='utf-8') as f:
    for i, line in enumerate(open(r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8')):
        if 'class SettingsScreen' in line:
            obj = json.loads(line)
            if 'content' in obj:
                content = obj['content']
                if len(content) > 10000:
                    f.write(f"--- Line {i} Length {len(content)} ---\n")
                    f.write(content[:1000] + "\n...[truncated]...\n")
                    f.write(content[-1000:] + "\n")
                    
