import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

import_statement = "import '../widgets/next_episode_tracker.dart';\n"
if import_statement not in text:
    text = text.replace("import '../widgets/animated_movie_logo.dart';", "import '../widgets/animated_movie_logo.dart';\n" + import_statement)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Added import")
