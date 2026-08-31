import os
import time

log_path = r"C:\Users\Asus\.gemini\antigravity\brain\d8a141a0-75a6-456a-81c4-4b145d433946\.system_generated\tasks\task-34656.log"
print("Waiting for dev release...")
for _ in range(60):
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "HOA,A N TAAAAT XUA,AA_T BA,AAN!" in content or "HOA,AN TA,AT" in content or "Hoan tat!" in content or "[6/6]" in content and "Done!" in content or "DONE!" in content or "File th?c thi t?i" in content:
            print("Dev Release finished!")
            break
    time.sleep(3)
