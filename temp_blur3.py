import re

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

# Reduce blur from 6.0 to 3.0
c = c.replace(
    "imageFilter: ImageFilter.blur(sigmaX: 6.0, sigmaY: 6.0), // Reduced blur as requested",
    "imageFilter: ImageFilter.blur(sigmaX: 3.0, sigmaY: 3.0), // Very light blur"
)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Reduced blur from 6 to 3")
