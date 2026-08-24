import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Fix actors mapping
old_actors = """           _actors = casts.take(15).map((c) => {
              'id': c['id']?.toString() ?? '',
              'name': c['name']?.toString() ?? '',
              'character': c['character']?.toString() ?? '',
              'profile_path': c['profile_path']?.toString() ?? '',
           }).toList();"""

new_actors = """           _actors = casts.take(15).map((c) => {
              'id': c['id']?.toString() ?? '',
              'name': c['name']?.toString() ?? '',
              'character': c['character']?.toString() ?? '',
              'profile': c['profile_path'] != null ? 'https://image.tmdb.org/t/p/w200${c['profile_path']}' : '',
           }).toList();"""

content = content.replace(old_actors, new_actors)

# Add Directors to _directors state? Wait, we already have _movie!.directors. 
# But the user said "đưa đạo diễn xuống dưới diễn viên". This means the UI should render directors as visual images below the actor list.
# Let's check how _actors are rendered first.
with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Actors fixed")
