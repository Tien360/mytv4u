import json
import codecs
log_file = r"C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl"
with codecs.open('yt_login_rest.txt', 'w', encoding='utf-8') as out:
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            if "child: Container(" in line and "Webview(" in line:
                data = json.loads(line)
                if "tool_calls" in data:
                    for tc in data["tool_calls"]:
                        args = str(tc.get("args", {}))
                        if "child: Container(" in args:
                            idx = args.find("child: Container(")
                            out.write(args[max(0, idx):min(len(args), idx+1000)] + "\n=====\n")
