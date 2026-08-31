import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_button = """class HoverEpisodeButton extends StatefulWidget {
  final String text;
  final VoidCallback onTap;

  const HoverEpisodeButton({
    super.key,
    required this.text,
    required this.onTap,
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
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              decoration: BoxDecoration(
                color: _isHovered
                    ? Colors.white.withOpacity(0.2)
                    : Colors.white.withOpacity(0.08),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: _isHovered
                      ? Colors.white.withOpacity(0.5)
                      : Colors.white.withOpacity(0.15),
                  width: 1,
                ),
              ),
              child: Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 12,
                ),
                child: Text(
                  widget.text,
                  style: TextStyle(
                    color: _isHovered ? Colors.white : Colors.white70,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}"""

new_button = """class HoverEpisodeButton extends StatefulWidget {
  final String text;
  final VoidCallback onTap;

  const HoverEpisodeButton({
    super.key,
    required this.text,
    required this.onTap,
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
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              decoration: BoxDecoration(
                color: _isHovered
                    ? Colors.white.withOpacity(0.2)
                    : Colors.white.withOpacity(0.08),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: _isHovered
                      ? Colors.white.withOpacity(0.5)
                      : Colors.white.withOpacity(0.15),
                  width: 1,
                ),
              ),
              child: Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 12,
                ),
                constraints: BoxConstraints(
                  maxWidth: _isHovered ? 600 : 200,
                ),
                child: AnimatedSize(
                  duration: const Duration(milliseconds: 200),
                  alignment: Alignment.centerLeft,
                  child: Text(
                    widget.text,
                    maxLines: _isHovered ? null : 1,
                    overflow: _isHovered ? TextOverflow.visible : TextOverflow.ellipsis,
                    softWrap: _isHovered,
                    style: TextStyle(
                      color: _isHovered ? Colors.white : Colors.white70,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}"""

# We have to replace whitespace robustly
content = re.sub(r'class HoverEpisodeButton extends StatefulWidget \{.*?\}(?=\nclass|\Z)', new_button, content, flags=re.DOTALL)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced HoverEpisodeButton")
