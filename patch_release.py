import re

path = r"T:\Project\Phim\mytv4u_flutter\tools\release.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's see where flutter build is called.
if "dart run tools/download_ytdlp.dart" not in content:
    content = content.replace("await autoTranslate();", "await autoTranslate();\n\n  print('[0/6] Tải công cụ lõi yt-dlp...');\n  final ytRes = await Process.run('dart', ['run', 'tools/download_ytdlp.dart']);\n  print(ytRes.stdout);")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched release.dart")
