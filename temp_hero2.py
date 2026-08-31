import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/gaming_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("child: CachedNetworkImage(", "child: Hero(tag: widget.game['url']!, child: CachedNetworkImage(")
content = content.replace("fit: BoxFit.cover,\n                        ),", "fit: BoxFit.cover,\n                        ),),")

with open('lib/screens/gaming_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
