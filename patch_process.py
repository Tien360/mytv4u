import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

old_cond = """      if (url.contains('workers.dev') ||
          (url.contains('dpdns.org') && !url.contains('stream/hls'))) {"""
          
new_cond = """      if ((url.contains('workers.dev') && !url.contains('stream/hls')) ||
          (url.contains('dpdns.org') && !url.contains('stream/hls'))) {"""

content = content.replace(old_cond, new_cond)

with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched processM3u8Url")
