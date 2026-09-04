import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

old_p2p = """                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 8,
                  ),
                  decoration: BoxDecoration(
                    color: isActive
                        ? Colors.blueAccent
                        : Colors.white.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    ep.name,
                    style: TextStyle(
                      color: isActive ? Colors.white : Colors.white70,
                    ),
                  ),
                ),"""

new_p2p = """                child: ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: Stack(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        decoration: BoxDecoration(
                          color: isActive ? Colors.blueAccent : Colors.white.withOpacity(0.1),
                        ),
                        child: Text(
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
                        ),
                    ],
                  ),
                ),"""

c = c.replace(old_p2p, new_p2p)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated P2P UI block")
