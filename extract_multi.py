import json
with open('all_multi_reps.txt', 'w', encoding='utf-8') as f:
    for i, line in enumerate(open(r'C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8')):
        if 'settings_screen.dart' in line:
            obj = json.loads(line)
            if 'tool_calls' in obj:
                for tc in obj['tool_calls']:
                    args = tc.get('args', {})
                    if 'settings_screen.dart' in str(args):
                        if tc['name'] == 'multi_replace_file_content':
                            f.write(f"\n{'='*40}\nTool Call: multi_replace_file_content at line {i}\n{'='*40}\n")
                            for rep in args.get('Replacements', []):
                                f.write("--- TARGET ---\n")
                                f.write(rep.get('TargetContent', ''))
                                f.write("\n--- REPLACEMENT ---\n")
                                f.write(rep.get('ReplacementContent', ''))
                                f.write("\n")
