import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/gaming_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import 'package:cached_network_image/cached_network_image.dart';", "")

import re
content = re.sub(r'Hero\(tag: widget.game\[\'url\'\]!, child: CachedNetworkImage\(\s*imageUrl: widget.game\[\'image\'\]!,\s*fit: BoxFit.cover,\s*\),\s*\),', 
r'''Hero(
  tag: widget.game['url']!,
  child: Image.network(
    widget.game['image']!,
    fit: BoxFit.cover,
  ),
)''', content)

with open('lib/screens/gaming_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("fixed gaming_screen.dart")

with open('lib/screens/game_detail_screen.dart', 'r', encoding='utf-8') as f:
    content2 = f.read()

content2 = content2.replace("import 'package:cached_network_image/cached_network_image.dart';", "")

content2 = re.sub(r'CachedNetworkImage\(\s*imageUrl: currentThumb,\s*width: 300,\s*height: 300,\s*fit: BoxFit.cover,\s*placeholder: \(context, url\) => Container\(\s*width: 300,\s*height: 300,\s*color: Colors.white10,\s*child: const Center\(child: CircularProgressIndicator\(\)\),\s*\),\s*\)',
r'''Image.network(
  currentThumb,
  width: 300,
  height: 300,
  fit: BoxFit.cover,
  loadingBuilder: (context, child, loadingProgress) {
    if (loadingProgress == null) return child;
    return Container(
      width: 300,
      height: 300,
      color: Colors.white10,
      child: const Center(child: CircularProgressIndicator()),
    );
  },
  errorBuilder: (context, error, stackTrace) => Container(
    width: 300,
    height: 300,
    color: Colors.white10,
    child: const Icon(Icons.error),
  ),
)''', content2)

with open('lib/screens/game_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content2)

print("fixed game_detail_screen.dart")
