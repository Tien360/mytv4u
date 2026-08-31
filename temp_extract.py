import json
with open('extracted_audio.txt', 'w', encoding='utf-8') as f:
    for line in open(r'C:\Users\Asus\.gemini\antigravity\brain\6745bc9b-1158-4c1a-9667-81aeae4807ef\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8'):
        if 'settings_screen.dart' in line:
            obj = json.loads(line)
            for tc in obj.get('tool_calls', []):
                args = tc.get('arguments', {})
                if 'ReplacementContent' in args:
                    f.write(args['ReplacementContent'] + '\n\n---\n\n')
                if 'CodeContent' in args:
                    f.write(args['CodeContent'] + '\n\n---\n\n')
