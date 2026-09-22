import re
for file_path in ["lib/screens/player_screen.dart", "lib/screens/yt_player_screen.dart"]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "premium_api.dart" not in content:
        content = content.replace("import '../api/phim_api.dart';", "import '../api/phim_api.dart';\nimport '../api/premium_api.dart';")

    content = content.replace("Uri.parse('https://medata.phim4k.workers.dev/?id=' + id),", """Uri.parse('${PremiumApi.medataDomain ?? 'https://medata.phim4k.workers.dev'}/?id=' + id),""")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Updated player screens")
