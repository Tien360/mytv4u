import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

builder_pattern = r'\s*Builder\(\s*builder: \(context\) \{\s*String msg = \'\';.*?return const SizedBox\.shrink\(\);\s*\}\s*\),'
text = re.sub(builder_pattern, '', text, flags=re.DOTALL)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Removed Builder code")
