import os
import time

log_path = r"C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\tasks\task-33809.log"
print("Waiting for build to finish...")
for _ in range(60):
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if lines:
            last_lines = "".join(lines[-15:])
            if "[3/6] Tao file cai dat (.exe) voi Inno Setup..." in last_lines or "[4/6]" in last_lines:
                print("Compiling Inno Setup...")
                break
    time.sleep(2)
