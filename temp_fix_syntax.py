import sys
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

target = """                                            _buildBadgeIcon(
                                              Icons.layers,
                                              episodeText,
                                            ),
                                                    ),
                                                  ),
                                                ),
                                              ],
                                            _buildBadgeIcon("""

replacement = """                                            _buildBadgeIcon(
                                              Icons.layers,
                                              episodeText,
                                            ),
                                            _buildBadgeIcon("""

if target in c:
    c = c.replace(target, replacement)
    print("Fixed leftover syntax error")
else:
    print("Target not found")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

