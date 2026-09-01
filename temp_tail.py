import re

with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Let's see if there are any other classes at the end of the file
tail = content[-500:]
print(tail)
