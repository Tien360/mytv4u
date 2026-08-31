import json
with open('all_settings_changes.txt', 'w', encoding='utf-8') as f:
    for line in open(r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8'):
        if 'settings_screen.dart' in line:
            obj = json.loads(line)
            if 'tool_calls' in obj:
                for tc in obj['tool_calls']:
                    args = tc.get('args', {})
                    if 'settings_screen.dart' in str(args):
                        f.write(f"--- Tool Call: {tc['name']} ---\n")
                        if 'CodeContent' in args:
                            f.write(f"CodeContent Length: {len(args['CodeContent'])}\n")
                        if 'ReplacementContent' in args:
                            f.write(f"ReplacementContent Length: {len(args['ReplacementContent'])}\n")
                            f.write(args['ReplacementContent'][:200] + "\n...\n")
                        if 'CommandLine' in args:
                            f.write(f"Command: {args['CommandLine'][:300]}\n")
                        f.write("\n")
