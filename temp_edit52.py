import sys

with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

# Add state variable
c = re.sub(
    r'(bool _showEpisodePanel = false;)',
    r'\1\n  int _selectedEpisodeChunk = 0;',
    c
)

# Update the toggle button
old_toggle = """                                                  onPressed: () => setState(
                                                    () => _showEpisodePanel =
                                                        !_showEpisodePanel,
                                                  ),"""
new_toggle = """                                                  onPressed: () => setState(
                                                    () {
                                                      _showEpisodePanel = !_showEpisodePanel;
                                                      if (_showEpisodePanel) {
                                                        _selectedEpisodeChunk = _currentIndex ~/ 50;
                                                      }
                                                    }
                                                  ),"""
c = c.replace(old_toggle, new_toggle)

# Update the modal UI
old_modal = """                          const Divider(color: Colors.white24, height: 32),
                          Expanded(
                            child: SingleChildScrollView(
                              child: Wrap(
                                spacing: 8,
                                runSpacing: 8,
                                children: _episodes.asMap().entries.map((entry) {
                                  final index = entry.key;
                                  final ep = entry.value;
                                  final isCurrent = index == _currentIndex;
                                  return PlayerEpisodeButton(
                                    episode: ep,
                                    isCurrent: isCurrent,
                                    movieName: widget.movieName,
                                    onTap: () {
                                      _initEpisode(index);
                                      setState(() => _showEpisodePanel = false);
                                    },
                                  );
                                }).toList(),
                              ),
                            ),
                          ),"""

new_modal = """                          const Divider(color: Colors.white24, height: 32),
                          if ((_episodes.length / 50).ceil() > 1) ...[
                            SingleChildScrollView(
                              scrollDirection: Axis.horizontal,
                              child: Row(
                                children: List.generate((_episodes.length / 50).ceil(), (chunkIdx) {
                                  final s = chunkIdx * 50 + 1;
                                  final e = (chunkIdx * 50 + 50 > _episodes.length) ? _episodes.length : chunkIdx * 50 + 50;
                                  final isActive = _selectedEpisodeChunk == chunkIdx;
                                  return Padding(
                                    padding: const EdgeInsets.only(right: 8.0, bottom: 16.0),
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
                          ],
                          Expanded(
                            child: SingleChildScrollView(
                              child: Wrap(
                                spacing: 8,
                                runSpacing: 8,
                                children: () {
                                  final chunkSize = 50;
                                  final maxChunks = (_episodes.length / chunkSize).ceil();
                                  int safeChunk = _selectedEpisodeChunk;
                                  if (safeChunk >= maxChunks) {
                                    safeChunk = 0;
                                  }
                                  final startIdx = safeChunk * chunkSize;
                                  final endIdx = (startIdx + chunkSize > _episodes.length) ? _episodes.length : startIdx + chunkSize;
                                  
                                  return _episodes.sublist(startIdx, endIdx).asMap().entries.map((entry) {
                                    final relativeIndex = entry.key;
                                    final index = startIdx + relativeIndex;
                                    final ep = entry.value;
                                    final isCurrent = index == _currentIndex;
                                    return PlayerEpisodeButton(
                                      episode: ep,
                                      isCurrent: isCurrent,
                                      movieName: widget.movieName,
                                      onTap: () {
                                        _initEpisode(index);
                                        setState(() => _showEpisodePanel = false);
                                      },
                                    );
                                  }).toList();
                                }(),
                              ),
                            ),
                          ),"""

c = c.replace(old_modal, new_modal)

with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Added chunking to PlayerScreen episode list")
