import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/game_detail_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("import 'package:cached_network_image/cached_network_image.dart';", "")

target = """                          child: CachedNetworkImage(
                            imageUrl: currentThumb,
                            width: 300,
                            height: 300,
                            fit: BoxFit.cover,
                            placeholder: (context, url) => Container(
                              width: 300,
                              height: 300,
                              color: Colors.white10,
                              child: const Center(child: CircularProgressIndicator()),
                            ),
                          ),"""
new_target = """                          child: Image.network(
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
                          ),"""
if target in c:
    c = c.replace(target, new_target)
    with open('lib/screens/game_detail_screen.dart', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed game_detail_screen.dart")
else:
    print("Could not find target in game_detail")
    
with open('lib/screens/gaming_screen.dart', 'r', encoding='utf-8') as f:
    c2 = f.read()
    
c2 = c2.replace("import 'package:cached_network_image/cached_network_image.dart';", "")

t2 = """                      child: Hero(tag: widget.game['url']!, child: CachedNetworkImage(
                        imageUrl: widget.game['image']!,
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),"""
nt2 = """                      child: Hero(
                        tag: widget.game['url']!,
                        child: Image.network(
                          widget.game['image']!,
                          fit: BoxFit.cover,
                        ),
                      ),
                    ),"""

if t2 in c2:
    c2 = c2.replace(t2, nt2)
    with open('lib/screens/gaming_screen.dart', 'w', encoding='utf-8') as f:
        f.write(c2)
    print("Fixed gaming_screen.dart")
else:
    print("Could not find t2 in gaming_screen")
