import re
with open(r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart", 'r', encoding='utf-8') as f:
    content = f.read()
match = re.search(r"class HoverEpisodeButton extends StatefulWidget \{.*?\}(?=\nclass|\z)", content, re.DOTALL)
if match:
    print(match.group(0))
