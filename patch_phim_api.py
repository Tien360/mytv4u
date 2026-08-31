import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\api\phim_api.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_ep_creation = """return Episode(
                  name: (ep['name'] ?? '').toString(),
                  slug: (ep['slug'] ?? '').toString(),
                  m3u8Url: processed,
                  embedUrl: (ep['link_embed'] ?? ep['embed'] ?? '').toString(),
                );"""

new_ep_creation = """return Episode(
                  name: (ep['name'] ?? '').toString(),
                  slug: (ep['slug'] ?? '').toString(),
                  m3u8Url: processed,
                  embedUrl: (ep['link_embed'] ?? ep['embed'] ?? '').toString(),
                  filename: (ep['filename'] ?? '').toString(),
                );"""

if old_ep_creation in content:
    content = content.replace(old_ep_creation, new_ep_creation)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated phim_api.dart Episode parsing")
else:
    print("Could not find Episode parsing in phim_api.dart")
