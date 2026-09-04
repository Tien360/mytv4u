import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

# P2P Series Episode (GestureDetector -> Stack)
# Find the exact text in P2P episodes
old_p2p = """                      child: Text(
                        ep.name,
                        style: TextStyle(color: isActive ? Colors.white : Colors.white70),
                      ),
                    ),"""
new_p2p = """                      child: Text(
                        ep.name,
                        style: TextStyle(color: isActive ? Colors.white : Colors.white70),
                      ),
                    ),
                    if ((_episodeProgressMap[ep.name] ?? 0.0) > 0)
                      Positioned(
                        bottom: 0, left: 0, right: 0,
                        child: Container(
                          height: 3,
                          alignment: Alignment.centerLeft,
                          child: FractionallySizedBox(
                            widthFactor: (_episodeProgressMap[ep.name] ?? 0.0).clamp(0.0, 1.0),
                            child: Container(color: _dominantColor),
                          ),
                        ),
                      ),"""
if old_p2p in c and new_p2p not in c:
    c = c.replace(old_p2p, new_p2p)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Injected P2P progress UI")
