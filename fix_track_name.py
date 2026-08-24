import re
with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"(if \(track\.title != null .*?\s+details\.add\('\[\$\{track\.language\}\]'\);\s+)(if \(details\.isEmpty\))"
replacement = r"\1try { if (track.channels != null) details.add('${track.channels}ch'); if (track.bitrate != null && track.bitrate > 0) details.add('${track.bitrate ~/ 1000}kbps'); } catch (_) {} \2"

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
if new_content != content:
    with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Replaced")
else:
    print("Not replaced")
