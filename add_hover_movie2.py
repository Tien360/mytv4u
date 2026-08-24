with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the part inside _AnimatedMovieLogoWidgetState
old_decl = "late int _animationType;"
new_decl = "late int _animationType;\n  bool _isHovered = false;"

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

if old_decl in text and old_child in text:
    text = text.replace(old_decl, new_decl)
    text = text.replace(old_child, new_child)
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Modified movie_detail_screen.dart!")
else:
    print("Could not find pattern in movie_detail_screen.dart")
