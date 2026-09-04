import sys

with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

old_ui = """                          if ((_episodes.length / 50).ceil() > 1) ...[
                            SingleChildScrollView(
                              scrollDirection: Axis.horizontal,
                              child: Row(
                                children: List.generate((_episodes.length / 50).ceil(), (chunkIdx) {"""

new_ui = """                          if ((_episodes.length / 50).ceil() > 1) ...[
                            Wrap(
                              spacing: 8.0,
                              runSpacing: 8.0,
                              children: List.generate((_episodes.length / 50).ceil(), (chunkIdx) {"""
c = c.replace(old_ui, new_ui)

old_ui2 = """                                    padding: const EdgeInsets.only(right: 8.0, bottom: 16.0),
                                    child: GestureDetector(
                                      onTap: () => setState(() => _selectedEpisodeChunk = chunkIdx),
                                      child: Container(
                                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                                        decoration: BoxDecoration(
                                          color: isActive ? Colors.blueAccent : Colors.white.withOpacity(0.1),
                                          borderRadius: BorderRadius.circular(8),
                                        ),
                                        child: Text(
                                          '$s - $e',
                                          style: TextStyle(
                                            color: isActive ? Colors.white : Colors.white70,
                                            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                                          ),
                                        ),
                                      ),
                                    ),
                                  );
                                }),
                              ),
                            ),
                          ],"""

new_ui2 = """                                    child: GestureDetector(
                                      onTap: () => setState(() => _selectedEpisodeChunk = chunkIdx),
                                      child: Container(
                                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                                        decoration: BoxDecoration(
                                          color: isActive ? Colors.blueAccent : Colors.white.withOpacity(0.1),
                                          borderRadius: BorderRadius.circular(8),
                                        ),
                                        child: Text(
                                          '$s - $e',
                                          style: TextStyle(
                                            color: isActive ? Colors.white : Colors.white70,
                                            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                                          ),
                                        ),
                                      ),
                                    ),
                                  );
                                }),
                            ),
                            const SizedBox(height: 16),
                          ],"""

c = c.replace(old_ui2, new_ui2)

with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Changed chunk selector to Wrap")
