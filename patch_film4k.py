import re

with open('lib/api/film4knet_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace: String serverName = src['label'] ?? 'Film4K Archive';
# With:    String rawLabel = src['label'] ?? 'Archive';
#          String serverName = "Film4kNet - " + rawLabel;

new_text = re.sub(
    r"String serverName = src\['label'\] \?\? 'Film4K Archive';",
    "String rawLabel = src['label'] ?? 'Archive';\n              String serverName = 'Film4kNet - ' + rawLabel;",
    text
)

with open('lib/api/film4knet_api.dart', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Fixed film4knet_api.dart")
