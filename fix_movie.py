import re

with open("lib/models/movie.dart", "r", encoding="utf-8") as f:
    text = f.read()

old_logic = """    final match = regex.firstMatch(parsedName);
    if (match != null) {
      parsedName = match.group(1)?.trim() ?? parsedName;"""

new_logic = """    final match = regex.firstMatch(parsedName);
    if (match != null) {
      String extractedName = match.group(1)?.trim() ?? '';
      if (extractedName.isNotEmpty) {
        parsedName = extractedName;
      }"""

if old_logic in text:
    text = text.replace(old_logic, new_logic)
    with open("lib/models/movie.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Fixed name regex wipeout in movie.dart!")
else:
    print("Old logic not found!")
