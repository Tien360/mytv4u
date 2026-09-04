with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

hover_def_old = """class HoverEpisodeButton extends StatefulWidget {
  final String text;
  final VoidCallback onTap;

  const HoverEpisodeButton({
    super.key,
    required this.text,
    required this.onTap,
  });"""

hover_def_new = """class HoverEpisodeButton extends StatefulWidget {
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
  });"""

c = c.replace(hover_def_old, hover_def_new)

hover_state_old = """        child: ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: isMinimalistUi.value 
            ? AnimatedContainer("""

hover_state_new = """        child: ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: Stack(
            children: [
              isMinimalistUi.value 
                ? AnimatedContainer("""

c = c.replace(hover_state_old, hover_state_new)

hover_state_old2 = """            ),
          ),
        ),
    );
  }
}"""

hover_state_new2 = """            ),
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
    );
  }
}"""

# Note: The ending might have different indentation. Let's do a regex replace.
c = re.sub(r'            \),\n          \),\n        \),\n    \);\n  \}\n\}', hover_state_new2, c)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated HoverEpisodeButton")
