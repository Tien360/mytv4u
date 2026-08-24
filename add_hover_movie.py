with open("AnimatedMovieLogoWidget.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Add _isHovered
text = text.replace("late int _animationType;", "late int _animationType;\n  bool _isHovered = false;")

# Wrap animatedChild in MouseRegion
old_child = """    return Container(
      constraints: const BoxConstraints(maxHeight: 120, maxWidth: 500),
      alignment: Alignment.centerLeft,
      margin: EdgeInsets.only(bottom: widget.showMainTitle ? 12 : 8),
      child: animatedChild,
    );"""

new_child = """    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      cursor: SystemMouseCursors.click,
      child: AnimatedScale(
        scale: _isHovered ? 1.05 : 1.0,
        duration: const Duration(milliseconds: 200),
        child: Container(
          constraints: const BoxConstraints(maxHeight: 120, maxWidth: 500),
          alignment: Alignment.centerLeft,
          margin: EdgeInsets.only(bottom: widget.showMainTitle ? 12 : 8),
          child: animatedChild,
        ),
      ),
    );"""

text = text.replace(old_child, new_child)
with open("AnimatedMovieLogoWidget.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Added hover to AnimatedMovieLogoWidget!")
