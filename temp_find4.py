import json
import codecs
log_file = r"C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl"
out = codecs.open("yt_sync_code.txt", "w", encoding="utf-8")
with open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        if "sync_yt" in line:
            data = json.loads(line)
            if "tool_calls" in data:
                for tc in data["tool_calls"]:
                    args = tc.get("args", {})
                    if "sync_yt" in str(args):
                        out.write(f"Tool: {tc['name']}\n")
                        out.write(str(args) + "\n=====\n")
out.close()
