import re

with open("lib/api/update_api.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Insert check inside checkForUpdate()
check_code = "  static Future<UpdateInfo?> checkForUpdate() async {\n    if (currentAppVersion.contains('.dev')) return null; // Dev builds never ask for updates\n\n    try {"
text = text.replace("  static Future<UpdateInfo?> checkForUpdate() async {\n    try {", check_code)

with open("lib/api/update_api.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated update_api.dart")
