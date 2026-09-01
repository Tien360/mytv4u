with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()
import re
m = re.search(r"(?s)void _showAirScheduleModal\(\).*?showDialog.*?\}\n  \}", c)
if m:
    with open("temp_modal.txt", "w", encoding="utf-8") as out:
        out.write(m.group(0))
    print("Exported to temp_modal.txt")
else:
    print("Not found")
