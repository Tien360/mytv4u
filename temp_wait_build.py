import os
import time

log_path = r"C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\tasks\task-33987.log"
print("Waiting for build to finish...")
for _ in range(30):
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "Built build" in content or "Build process failed" in content:
            print("Build finished!")
            break
    time.sleep(2)
