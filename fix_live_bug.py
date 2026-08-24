with open("lib/api/sport_api.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Fix the live status detection bug
old_check = "if (statusBadge != null && statusBadge.text.toLowerCase().contains('live')) {"
new_check = "if (statusBadge != null && statusBadge.classes.contains('status-live')) {"
text = text.replace(old_check, new_check)

with open("lib/api/sport_api.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed live bug!")
