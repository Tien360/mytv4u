import re

with open("lib/api/premium_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(r"\$", "$")

with open("lib/api/premium_api.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("premium_api.dart cleaned up literal \$")
