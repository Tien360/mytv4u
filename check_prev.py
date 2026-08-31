import json
import glob

folders = [
    r"C:\Users\Asus\.gemini\antigravity\brain\f235fc4e-d263-4f3b-be6d-e68a3ce83665",
    r"C:\Users\Asus\.gemini\antigravity\brain\4a6ffef4-11f0-4759-8775-a338defcb6b4",
    r"C:\Users\Asus\.gemini\antigravity\brain\32621995-2562-41be-a9cb-0301277cccdb",
    r"C:\Users\Asus\.gemini\antigravity\brain\41ba6571-a13f-404f-b4bc-4fbecb6c18bf"
]

for folder in folders:
    transcript = folder + r"\.system_generated\logs\transcript_full.jsonl"
    print(f"Checking {folder}")
    try:
        for i, line in enumerate(open(transcript, 'r', encoding='utf-8')):
            if 'settings_screen.dart' in line:
                obj = json.loads(line)
                if 'tool_calls' in obj:
                    for tc in obj['tool_calls']:
                        args = tc.get('args', {})
                        if 'settings_screen.dart' in str(args):
                            if 'CodeContent' in args:
                                print(f"  Line {i}: Found CodeContent len {len(args['CodeContent'])}")
                            if 'ReplacementContent' in args:
                                print(f"  Line {i}: Found ReplacementContent len {len(args['ReplacementContent'])}")
    except Exception as e:
        print(f"Error: {e}")
