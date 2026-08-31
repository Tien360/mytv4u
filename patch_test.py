import re
import sys

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Video via regex
video_regex = r"(else\s+Center\(\s+child:\s+Video\(\s+controller:\s+controller,\s+controls:\s+NoVideoControls,[^\)]+\),\s*\n\s*\),\s*\n\s*\),\s*\n\s*\),)"
# Actually, a simpler regex to grab the whole block:
video_regex = r"(else\s+Center\(\s+child:\s+Video\([^;]+?\),\s*\n\s*\),)"
match = re.search(r"(else\s*Center\(\s*child:\s*Video\([\s\S]+?\),\s*\n\s*\),)", content)

if match:
    original = match.group(1)
    
    # We replace `child: Video(...)` with `child: Stack(...)`
    # We find the inner Video() part
    inner_video_match = re.search(r"(Video\([\s\S]+?\),\s*\n\s*  ),)", original)
    if inner_video_match:
        inner = inner_video_match.group(1)
        print("Found inner")
else:
    print("Failed to find Video")

