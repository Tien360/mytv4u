import re

with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Find the build method of PlayerScreen to see if there is a variable for hasVideo
# Let's search for "Widget build(BuildContext context) {" inside _PlayerScreenState
