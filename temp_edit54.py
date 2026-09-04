import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

old_ui = """            if (maxChunks > 1) ...[
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: List.generate(maxChunks, (chunkIdx) {"""

new_ui = """            if (maxChunks > 1) ...[
              Wrap(
                spacing: 8.0,
                runSpacing: 8.0,
                children: List.generate(maxChunks, (chunkIdx) {"""
c = c.replace(old_ui, new_ui)

old_ui2 = """                    return Padding(
                      padding: const EdgeInsets.only(right: 8.0, bottom: 12.0),
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

new_ui2 = """                    return GestureDetector(
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
                    );
                  }),
              ),
              const SizedBox(height: 12),
            ],"""

c = c.replace(old_ui2, new_ui2)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Changed chunk selector to Wrap in MovieDetailScreen")
