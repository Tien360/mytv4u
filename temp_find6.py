import json
log_file = r"C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\logs\transcript_full.jsonl"
with open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        if "method_new = " in line and "Timer.periodic" in line:
            data = json.loads(line)
            if "tool_calls" in data:
                for tc in data["tool_calls"]:
                    args = str(tc.get("args", {}))
                    if "method_new =" in args:
                        idx = args.find("method_new = ")
                        print(args[max(0, idx):min(len(args), idx+2000)].encode('utf-8').decode('unicode_escape'))
                        print("=====")
                        break
