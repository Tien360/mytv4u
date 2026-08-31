import os
import time

log_path = r"C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\tasks\task-33809.log"
print("Waiting for release to finish...")
for _ in range(30):
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "HOA,A N TAAAAT XUA,AA_T BA,AAN!" in content or "HOA,AN TA,AT" in content or "Hoan tat!" in content or "[6/6]" in content and "Done!" in content or "DONE!" in content:
            print("Release finished!")
            break
        if "[4/6]" in content[-1000:]:
            print("Uploading to GitHub...")
    time.sleep(3)
