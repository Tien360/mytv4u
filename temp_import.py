with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = "import 'dart:async';\n" + c

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Imported dart:async")
