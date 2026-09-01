with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

import_statement = "import '../widgets/air_schedule_dialog.dart';"
if import_statement not in c:
    c = c.replace("import '../widgets/glass_container.dart';", "import '../widgets/glass_container.dart';\n" + import_statement)

import re

# Replace the body of _showAirScheduleModal
old_func_pattern = r"(?s)void _showAirScheduleModal\(\).*?showDialog\([\s\S]*?\}\n  \}"
new_func = """  void _showAirScheduleModal() {
    showDialog(
      context: context,
      builder: (context) {
        return AirScheduleDialog(tmdbDetails: _tmdbDetails!);
      },
    );
  }"""
c = re.sub(old_func_pattern, new_func, c)

# Also remove _fetchAirSchedule because it's no longer needed in this file
fetch_pattern = r"(?s)Future<List<dynamic>> _fetchAirSchedule\(\) async \{[\s\S]*?\}\n    \}"
c = re.sub(fetch_pattern, "", c)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated movie_detail_screen_test.dart!")
