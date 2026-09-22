import re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add import if missing
if "premium_api.dart" not in content:
    content = content.replace("import '../api/phim_api.dart';", "import '../api/phim_api.dart';\nimport '../api/premium_api.dart';")

# Ensure _initCache is called or just use the getter directly (since movie details screen is opened, PremiumApi._initCache was likely called already, but let's call ensureInit)
content = content.replace("Uri.parse('https://medata.phim4k.workers.dev/?id=$id'),", """Uri.parse('${PremiumApi.medataDomain ?? 'https://medata.phim4k.workers.dev'}/?id=$id'),""")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated movie_detail_screen.dart")
