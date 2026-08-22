
import re

with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace border radius 12 with 24 for all ElevatedButtons in the action row
# (around line 1230-1410)
# We can just do a regex replace for BorderRadius.circular(12) in that specific section.

new_content = re.sub(
    r'BorderRadius\.circular\(12\)',
    r'BorderRadius.circular(24)',
    content
)

with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Updated border radius')

