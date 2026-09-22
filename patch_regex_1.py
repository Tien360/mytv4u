import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# We want to replace:
# if (uri != null && uri.pathSegments.isNotEmpty) {
#   // Đánh giá chất lượng từ tên file/server (vd: 2160p, 1080p, 4K)
#   ...
#   'id': uri.pathSegments.last,

pattern = re.compile(
    r"if\s*\(uri\s*!=\s*null\s*&&\s*uri\.pathSegments\.isNotEmpty\)\s*\{(.+?)'id':\s*uri\.pathSegments\.last,",
    re.DOTALL
)

def repl(match):
    inner = match.group(1)
    return """if (uri != null) {
              String rawId = uri.scheme == 'premium' ? uri.host : (uri.pathSegments.isNotEmpty ? uri.pathSegments.last : '');
              if (rawId.isNotEmpty) {""" + inner + "'id': rawId,"

content = pattern.sub(repl, content)

# Also fix the closing brace since we added one level of if.
# But wait, it was `if (A && B) { ... }`, we changed to `if (A) { if (B) { ... } }`. We need an extra closing brace!
# Let's just find the end of the block.
# Actually, the easier way is to just replace:
# if (uri != null && uri.pathSegments.isNotEmpty) {
# with:
# String rawId = uri != null ? (uri.scheme == 'premium' ? uri.host : (uri.pathSegments.isNotEmpty ? uri.pathSegments.last : '')) : '';
# if (rawId.isNotEmpty) {
# And replace uri.pathSegments.last with rawId!

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Regex patch applied for movie_detail_screen.dart?")
