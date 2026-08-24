import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# We need to find the start of the block and end of the block.
# Start: "if (_tmdbDetails!['next_episode_to_air'] != null && _tmdbDetails!['next_episode_to_air']['air_date'] != null) ...["
# End: "if (_tmdbDetails!['budget'] != null"

match = re.search(r'(if \(_tmdbDetails!\[\'next_episode_to_air\'\] != null.*?)\s*if \(_tmdbDetails!\[\'budget\'\] != null', text, re.DOTALL)
if match:
    print("Found block of length:", len(match.group(1)))
else:
    print("Not found")
