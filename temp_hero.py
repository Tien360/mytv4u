import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/gaming_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

old_img = """                      child: ClipRRect(
                        borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                        child: CachedNetworkImage(
                          imageUrl: widget.game['image']!,
                          fit: BoxFit.cover,
                        ),
                      ),"""

new_img = """                      child: Hero(
                        tag: widget.game['url']!,
                        child: ClipRRect(
                          borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                          child: CachedNetworkImage(
                            imageUrl: widget.game['image']!,
                            fit: BoxFit.cover,
                          ),
                        ),
                      ),"""

if old_img in content:
    content = content.replace(old_img, new_img)
    with open('lib/screens/gaming_screen.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added Hero tag to gaming_screen.dart")
else:
    print("Could not find image in gaming_screen")
