import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

search = """                          Expanded(
                            child: SingleChildScrollView(
                              child: Wrap(
                                spacing: 8,
                                runSpacing: 8,
                                children: widget.episodes.asMap().entries.map((
                                  entry,
                                ) {
                                  final index = entry.key;
                                  final ep = entry.value;
                                  final isCurrent = index == _currentIndex;
                                  return Material(
                                    color: Colors.transparent,
                                    child: InkWell(
                                      borderRadius: BorderRadius.circular(8),
                                      onTap: () {
                                        _initEpisode(index);
                                        setState(
                                          () => _showEpisodePanel = false,
                                        );
                                      },
                                      child: Container(
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 16,
                                          vertical: 10,
                                        ),
                                        decoration: BoxDecoration(
                                          color: isCurrent
                                              ? Colors.blueAccent.withValues(
                                                  alpha: 0.4,
                                                )
                                              : Colors.white10,
                                          borderRadius: BorderRadius.circular(
                                            8,
                                          ),
                                          border: Border.all(
                                            color: isCurrent
                                                ? Colors.blueAccent
                                                : Colors.transparent,
                                          ),
                                        ),
                                        child: Text(
                                          ep.name,
                                          style: TextStyle(
                                            color: isCurrent
                                                ? Colors.blueAccent
                                                : Colors.white,
                                            fontWeight: isCurrent
                                                ? FontWeight.bold
                                                : FontWeight.normal,
                                          ),
                                        ),
                                      ),
                                    ),
                                  );
                                }).toList(),
                              ),
                            ),
                          ),"""

new_logic = """                          Expanded(
                            child: ListView.separated(
                              padding: const EdgeInsets.only(top: 8),
                              itemCount: widget.episodes.length,
                              separatorBuilder: (_, __) => const SizedBox(height: 8),
                              itemBuilder: (context, index) {
                                final ep = widget.episodes[index];
                                final isCurrent = index == _currentIndex;
                                final hasThumb = ep.embedUrl.contains('ytimg.com');
                                return Material(
                                  color: Colors.transparent,
                                  child: InkWell(
                                    borderRadius: BorderRadius.circular(8),
                                    onTap: () {
                                      _initEpisode(index);
                                      setState(() => _showEpisodePanel = false);
                                    },
                                    child: Container(
                                      padding: const EdgeInsets.all(8),
                                      decoration: BoxDecoration(
                                        color: isCurrent ? Colors.blueAccent.withValues(alpha: 0.2) : Colors.white10,
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(color: isCurrent ? Colors.blueAccent : Colors.transparent),
                                      ),
                                      child: Row(
                                        children: [
                                          if (hasThumb) ...[
                                            ClipRRect(
                                              borderRadius: BorderRadius.circular(6),
                                              child: Image.network(
                                                ep.embedUrl.replaceAll('maxresdefault', 'mqdefault'), 
                                                width: 100, 
                                                height: 56, 
                                                fit: BoxFit.cover,
                                                errorBuilder: (c,e,s) => Container(width: 100, height: 56, color: Colors.grey[900]),
                                              ),
                                            ),
                                            const SizedBox(width: 12),
                                          ],
                                          Expanded(
                                            child: Text(
                                              ep.name,
                                              maxLines: 3,
                                              overflow: TextOverflow.ellipsis,
                                              style: TextStyle(
                                                color: isCurrent ? Colors.blueAccent : Colors.white,
                                                fontWeight: isCurrent ? FontWeight.bold : FontWeight.normal,
                                                fontSize: 14,
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                );
                              },
                            ),
                          ),"""

if search in content:
    content = content.replace(search, new_logic)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched UI successfully.")
else:
    print("Search block not found.")
