import json
import codecs

with open('missing.json', 'r', encoding='utf-8') as f:
    missing = json.load(f)
with open('updates.json', 'r', encoding='utf-8') as f:
    updates = json.load(f)

with codecs.open('missing_details.txt', 'w', encoding='utf-8') as f:
    f.write("### Kênh mới cần bổ sung:\n")
    for m in missing:
        f.write(f"- {m['name']} (Nhóm: {m.get('group', 'TV')})\n")

    f.write("\n### Kênh cần cập nhật Logo:\n")
    for k, v in updates.items():
        f.write(f"- {k} -> {v['m3u_name']}\n")
