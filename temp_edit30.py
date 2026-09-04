import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

# First, define the exact block that was wrongly injected multiple times
injected_block = """                if (widget.progress > 0)
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
            ),"""

# The bad replace was replacing `                ),\n              ),\n            ),` with the above + that original string.
# Wait, look at lines 2527-2528: `              ],\n            ),`

# Let's just find and remove the badly injected blocks that end in `], ),`
bad_block = """                if (widget.progress > 0)
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
            ),"""

c = c.replace(bad_block, "")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Removed bad blocks")
