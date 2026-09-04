with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

# Replace the build method of HoverEpisodeButton
new_build = """  @override
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
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                      ),
                    ),
                  )
                : BackdropFilter(
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
  }"""

c = re.sub(r'@override\s*Widget build\(BuildContext context\) \{\s*return MouseRegion\([\s\S]*?BackdropFilter\([\s\S]*?padding: const EdgeInsets\.symmetric\([\s\S]*?child: Text\([\s\S]*?\}\),\s*\}\),\s*\),\s*\),\s*\),\s*\),\s*\);\s*\}', new_build, c)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Replaced HoverEpisodeButton build method")
