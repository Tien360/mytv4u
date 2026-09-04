import sys
import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Replace class definition and constructor using regex
c = re.sub(
    r'class HoverEpisodeButton extends StatefulWidget \{.*?\n  const HoverEpisodeButton\(\{.*?\n    this\.progressColor = Colors\.redAccent,\n  \}\);',
    r'''class HoverEpisodeButton extends StatefulWidget {
  final String text;
  final VoidCallback onTap;
  final double progress;
  final Color progressColor;
  final String? episodeKey;
  final String? durationKey;

  const HoverEpisodeButton({
    super.key,
    required this.text,
    required this.onTap,
    this.progress = 0.0,
    this.progressColor = Colors.redAccent,
    this.episodeKey,
    this.durationKey,
  });''',
    c,
    flags=re.DOTALL
)

# Replace the state class completely
c = re.sub(
    r'class _HoverEpisodeButtonState extends State<HoverEpisodeButton> \{.*?    \);\n  \}\n\}',
    r'''class _HoverEpisodeButtonState extends State<HoverEpisodeButton> {
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
}''',
    c,
    flags=re.DOTALL
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated HoverEpisodeButton successfully with regex")
