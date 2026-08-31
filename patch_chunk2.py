import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add state variable
if "int _selectedEpisodeChunk = 0;" not in content:
    content = content.replace("int _visibleComments = 5;", "int _visibleComments = 5;\n  int _selectedEpisodeChunk = 0;")

new_logic = """    if (!hasSeasons) {
      final items = _currentServer!.items;
      final int chunkSize = 50;
      final int maxChunks = (items.length / chunkSize).ceil();
      
      // Ensure chunk index is valid
      if (_selectedEpisodeChunk >= maxChunks) {
        _selectedEpisodeChunk = 0;
      }
      
      final int startIdx = _selectedEpisodeChunk * chunkSize;
      final int endIdx = (startIdx + chunkSize > items.length) ? items.length : startIdx + chunkSize;
      final chunkItems = items.sublist(startIdx, endIdx);

      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (maxChunks > 1) ...[
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: List.generate(maxChunks, (chunkIdx) {
                  final s = chunkIdx * chunkSize + 1;
                  final e = (chunkIdx * chunkSize + chunkSize > items.length) ? items.length : chunkIdx * chunkSize + chunkSize;
                  final isActive = _selectedEpisodeChunk == chunkIdx;
                  return Padding(
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
                          f'{s} - {e}',
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
          Wrap(
            spacing: 12,
            runSpacing: 12,
            children: chunkItems.asMap().entries.map((entry) {
              // We need the true global index for PlayerScreen
              final index = startIdx + entry.key;
              final ep = entry.value;

              String dispName = ep.name;
              if (ep.filename != null && ep.filename!.isNotEmpty) {
                var q = _parseQualityFromFilename(ep.filename!);
                List<String> tags = [];
                if (q['hdr']!.isNotEmpty) tags.add(q['hdr']!);
                if (q['audio']!.isNotEmpty) tags.add(q['audio']!);
                if (tags.isNotEmpty) {
                  dispName += ' • ${tags.join(' ')}';
                }
              }

              return HoverEpisodeButton(
                text: dispName,
                onTap: () async {
                  _pauseTrailer();
                  FirebaseApi.saveContinueWatching(_movie!, ep.name);
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => PlayerScreen(
                        episodes: items,
                        currentEpisodeIndex: index,
                        movieName: _movie!.name,
                        imdbId: _movie!.imdbId,
                      ),
                    ),
                  );
                },
              );
            }).toList(),
          ),
        ],
      );
    }
"""

# Convert f-string f'{s} - {e}' to Dart string interpolation
new_logic = new_logic.replace("f'{s} - {e}'", "'$s - $e'")

pattern = r"    if \(\!hasSeasons\) \{[\s\S]*?\}\s*// P2P TV Series UI"

if re.search(pattern, content):
    content = re.sub(pattern, new_logic + "    // P2P TV Series UI", content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Chunk logic applied via regex!")
else:
    print("Regex failed to find block!")
