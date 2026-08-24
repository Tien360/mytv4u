import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Locate the Builder block
builder_pattern = r'Builder\(\s*builder: \(context\) \{\s*String msg = \'\';.*?return const SizedBox\.shrink\(\);\s*\}\s*\),'
match = re.search(builder_pattern, text, flags=re.DOTALL)
if match:
    builder_code = match.group(0)
    print("Found builder code!")
else:
    print("Builder code not found!")

