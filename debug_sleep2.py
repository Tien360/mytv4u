import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '_showSleepTimerDialog' in line:
        for j in range(i, i+60):
            if j < len(lines):
                print(f"{j}: {lines[j].rstrip()}")
        break
