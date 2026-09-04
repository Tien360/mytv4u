with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re
old = """            ],
          ),
        ),
    );
  }
}"""

new = """            ],
          ),
        ),
      ),
    );
  }
}"""
c = c.replace(old, new)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed brackets")
