import json

with open('get_contents.txt', 'w', encoding='utf-8') as f:
    for i, line in enumerate(open(r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8')):
        if 'settings_screen.dart' in line:
            obj = json.loads(line)
            if 'tool_calls' in obj:
                for tc in obj['tool_calls']:
                    args = tc.get('args', {})
                    if 'CommandLine' in args and 'settings_screen.dart' in args['CommandLine']:
                        f.write(f"Line {i}: {args['CommandLine'][:100]}\n")
            if obj.get('source') == 'MODEL' and obj.get('type') == 'RUN_COMMAND':
                # wait, this is not how it is structured
                pass
