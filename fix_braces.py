with open("lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("                          }\n                      style: ElevatedButton.styleFrom(", "                          }\n                      },\n                      style: ElevatedButton.styleFrom(")

with open("lib/screens/library_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
