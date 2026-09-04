import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Find HoverEpisodeButton class and state
old_button = """class HoverEpisodeButton extends StatefulWidget {
  final String text;
  final VoidCallback onTap;
  final double progress;
  final Color progressColor;

  const HoverEpisodeButton({
    super.key,
    required this.text,
    required this.onTap,
    this.progress = 0.0,
    this.progressColor = Colors.redAccent,
  });

  @override
  State<HoverEpisodeButton> createState() => _HoverEpisodeButtonState();
}

class _HoverEpisodeButtonState extends State<HoverEpisodeButton> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        onTap: widget.onTap,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: Stack(
            children: [
              isMinimalistUi.value 
                ? AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    decoration: BoxDecoration(
                      color: _isHovered
                          ? const Color(0xFF2A2A2A)
                          : const Color(0xFF1E1E1E),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(
                        color: _isHovered
                            ? Colors.white.withOpacity(0.5)
                            : Colors.white.withOpacity(0.1),
                      ),
                    ),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    child: Text(
                      widget.text,
                      style: TextStyle(
                        color: _isHovered ? Colors.white : Colors.white70,
                        fontWeight: _isHovered ? FontWeight.bold : FontWeight.normal,
                      ),
                    ),
                  )
                : AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    color: _isHovered
                        ? Colors.white.withOpacity(0.1)
                        : Colors.white.withOpacity(0.05),
                    child: Text(
                      widget.text,
                      style: const TextStyle(color: Colors.white),
                    ),
                  ),
              if (widget.progress > 0)
                Positioned(
                  bottom: 0, left: 0, right: 0,
                  child: Container(
                    height: 3,
                    alignment: Alignment.centerLeft,
                    child: FractionallySizedBox(
                      widthFactor: widget.progress.clamp(0.0, 1.0),
                      child: Container(color: widget.progressColor),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}"""

new_button = """class HoverEpisodeButton extends StatefulWidget {
  final String text;
  final VoidCallback onTap;
  final double progress;
  final Color progressColor;
  final String? episodeKey; // The exact key to lookup in SharedPreferences
  final String? durationKey; // The exact duration key

  const HoverEpisodeButton({
    super.key,
    required this.text,
    required this.onTap,
    this.progress = 0.0,
    this.progressColor = Colors.redAccent,
    this.episodeKey,
    this.durationKey,
  });

  @override
  State<HoverEpisodeButton> createState() => _HoverEpisodeButtonState();
}

class _HoverEpisodeButtonState extends State<HoverEpisodeButton> {
  bool _isHovered = false;
  double _localProgress = 0.0;

  @override
  void initState() {
    super.initState();
    _localProgress = widget.progress;
    _loadDirectProgress();
  }

  @override
  void didUpdateWidget(covariant HoverEpisodeButton oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.progress != oldWidget.progress || widget.episodeKey != oldWidget.episodeKey) {
      _localProgress = widget.progress;
      _loadDirectProgress();
    }
  }

  Future<void> _loadDirectProgress() async {
    if (widget.episodeKey == null) return;
    try {
      final prefs = await SharedPreferences.getInstance();
      final posMs = prefs.getInt(widget.episodeKey!) ?? 0;
      if (posMs > 0) {
        int durMs = 0;
        if (widget.durationKey != null) {
          durMs = prefs.getInt(widget.durationKey!) ?? 0;
        }
        double fraction = 0.05;
        if (durMs > 0) {
          fraction = (posMs / durMs).clamp(0.0, 1.0);
        }
        if (fraction > 0 && fraction < 0.05) fraction = 0.05;
        if (mounted) {
          setState(() {
            _localProgress = fraction;
          });
        }
      }
    } catch (e) {}
  }

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        onTap: widget.onTap,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: Stack(
            children: [
              isMinimalistUi.value 
                ? AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    decoration: BoxDecoration(
                      color: _isHovered
                          ? const Color(0xFF2A2A2A)
                          : const Color(0xFF1E1E1E),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(
                        color: _isHovered
                            ? Colors.white.withOpacity(0.5)
                            : Colors.white.withOpacity(0.1),
                      ),
                    ),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    child: Text(
                      widget.text,
                      style: TextStyle(
                        color: _isHovered ? Colors.white : Colors.white70,
                        fontWeight: _isHovered ? FontWeight.bold : FontWeight.normal,
                      ),
                    ),
                  )
                : AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    color: _isHovered
                        ? Colors.white.withOpacity(0.1)
                        : Colors.white.withOpacity(0.05),
                    child: Text(
                      widget.text,
                      style: const TextStyle(color: Colors.white),
                    ),
                  ),
              if (_localProgress > 0)
                Positioned(
                  bottom: 0, left: 0, right: 0,
                  child: Container(
                    height: 3,
                    alignment: Alignment.centerLeft,
                    child: FractionallySizedBox(
                      widthFactor: _localProgress.clamp(0.0, 1.0),
                      child: Container(color: widget.progressColor),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}"""

c = c.replace(old_button, new_button)

# Now update the HoverEpisodeButton calls to pass episodeKey and durationKey
import re

# Update standard episodes
c = re.sub(
    r'return HoverEpisodeButton\(\s*text: dispName,\s*progress: _episodeProgressMap\[ep\.name\] \?\? 0\.0,\s*progressColor: _dominantColor,',
    r"return HoverEpisodeButton(\n                  text: dispName,\n                  progress: _episodeProgressMap[ep.name] ?? 0.0,\n                  episodeKey: 'continue_${_movie!.name}_${ep.name}',\n                  durationKey: 'continue_duration_${_movie!.name}_${ep.name}',\n                  progressColor: _dominantColor,",
    c
)

# Update p2p streams
c = re.sub(
    r"return HoverEpisodeButton\(\s*text: stream\.name,\s*progress: _episodeProgressMap\['\$\\{_selectedP2pEpisode!\.slug\\} - \$\\{stream\.name\\}'\] \?\? 0\.0,\s*progressColor: _dominantColor,",
    r"return HoverEpisodeButton(\n                  text: stream.name,\n                  progress: _episodeProgressMap['${_selectedP2pEpisode!.slug} - ${stream.name}'] ?? 0.0,\n                  episodeKey: 'continue_${_movie!.name}_${_selectedP2pEpisode!.slug} - ${stream.name}',\n                  durationKey: 'continue_duration_${_movie!.name}_${_selectedP2pEpisode!.slug} - ${stream.name}',\n                  progressColor: _dominantColor,",
    c
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated HoverEpisodeButton to load progress directly from SharedPreferences")
