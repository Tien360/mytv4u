import sys

with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

# We need to replace the mapping logic inside the Wrap:
# children: _episodes.asMap().entries.map((entry) { ... }).toList(),

old_map = """                              child: Wrap(
                                spacing: 8,
                                runSpacing: 8,
                                children: _episodes.asMap().entries.map((
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
                                        child: Row(
                                            children: [
                                              if (ep.embedUrl.startsWith('https://i.ytimg.com/')) ...[
                                                ClipRRect(
                                                  borderRadius: BorderRadius.circular(6),
                                                  child: Image.network(
                                                    ep.embedUrl,
                                                    width: 100,
                                                    height: 56,
                                                    fit: BoxFit.cover,
                                                    errorBuilder: (context, error, stackTrace) => const SizedBox(width: 100, height: 56, child: Icon(Icons.error, color: Colors.white30)),
                                                  ),
                                                ),
                                                const SizedBox(width: 12),
                                              ],
                                              Expanded(
                                                child: Text(
                                                  ep.name,
                                                  style: TextStyle(
                                                    color: isCurrent
                                                        ? Colors.blueAccent
                                                        : Colors.white,
                                                    fontWeight: isCurrent
                                                        ? FontWeight.bold
                                                        : FontWeight.normal,
                                                    height: 1.3,
                                                  ),
                                                  maxLines: 2,
                                                  overflow: TextOverflow.ellipsis,
                                                ),
                                              ),
                                            ],
                                          ),
                                      ),
                                    ),
                                  );
                                }).toList(),
                              ),"""

new_map = """                              child: Wrap(
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
                              ),"""

c = c.replace(old_map, new_map)

# Append PlayerEpisodeButton to the end of the file
new_class = """
class PlayerEpisodeButton extends StatefulWidget {
  final Episode episode;
  final bool isCurrent;
  final String movieName;
  final VoidCallback onTap;

  const PlayerEpisodeButton({
    super.key,
    required this.episode,
    required this.isCurrent,
    required this.movieName,
    required this.onTap,
  });

  @override
  State<PlayerEpisodeButton> createState() => _PlayerEpisodeButtonState();
}

class _PlayerEpisodeButtonState extends State<PlayerEpisodeButton> {
  double _progress = 0.0;

  @override
  void initState() {
    super.initState();
    _loadProgress();
  }
  
  @override
  void didUpdateWidget(covariant PlayerEpisodeButton oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.episode.name != oldWidget.episode.name) {
      _loadProgress();
    }
  }

  Future<void> _loadProgress() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final epKey = 'continue_${widget.movieName}_${widget.episode.name}';
      final durKey = 'continue_duration_${widget.movieName}_${widget.episode.name}';
      
      final posMs = prefs.getInt(epKey) ?? 0;
      if (posMs > 0) {
        final durMs = prefs.getInt(durKey) ?? 0;
        double fraction = 0.05;
        if (durMs > 0) {
          fraction = (posMs / durMs).clamp(0.0, 1.0);
        }
        if (fraction > 0 && fraction < 0.05) fraction = 0.05;
        if (mounted) {
          setState(() {
            _progress = fraction;
          });
        }
      }
    } catch (e) {}
  }

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: widget.onTap,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: Stack(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                decoration: BoxDecoration(
                  color: widget.isCurrent
                      ? Colors.blueAccent.withOpacity(0.4)
                      : Colors.white10,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(
                    color: widget.isCurrent ? Colors.blueAccent : Colors.transparent,
                  ),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    if (widget.episode.embedUrl.startsWith('https://i.ytimg.com/')) ...[
                      ClipRRect(
                        borderRadius: BorderRadius.circular(6),
                        child: Image.network(
                          widget.episode.embedUrl,
                          width: 100,
                          height: 56,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) => const SizedBox(
                              width: 100, height: 56, child: Icon(Icons.error, color: Colors.white30)),
                        ),
                      ),
                      const SizedBox(width: 12),
                    ],
                    Text(
                      widget.episode.name,
                      style: TextStyle(
                        color: widget.isCurrent ? Colors.blueAccent : Colors.white,
                        fontWeight: widget.isCurrent ? FontWeight.bold : FontWeight.normal,
                        height: 1.3,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              if (_progress > 0)
                Positioned(
                  bottom: 0,
                  left: 0,
                  right: 0,
                  child: Container(
                    height: 3,
                    alignment: Alignment.centerLeft,
                    child: FractionallySizedBox(
                      widthFactor: _progress.clamp(0.0, 1.0),
                      child: Container(color: Colors.redAccent),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
"""

if "PlayerEpisodeButton" not in c:
    c = c + new_class

with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated PlayerScreen to use PlayerEpisodeButton with progress bar")
