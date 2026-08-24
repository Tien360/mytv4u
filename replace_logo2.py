import re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

pattern = r"Container\(\s*padding: const EdgeInsets\.symmetric\(horizontal: 8, vertical: 4\),\s*decoration: BoxDecoration\(\s*color: Colors\.white,\s*borderRadius: BorderRadius\.circular\(4\),\s*\),\s*child: Image\.network\(\s*'https://image\.tmdb\.org/t/p/w200\$\{c\['logo_path'\]\}',\s*height: 24,\s*fit: BoxFit\.contain,\s*\),\s*\)"

new_widget = "AnimatedLogoWidget(logoPath: c['logo_path'])"

if re.search(pattern, text):
    text = re.sub(pattern, new_widget, text)
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Replaced with AnimatedLogoWidget!")
else:
    print("Could not find pattern!")
