with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("List<Map<String, String>> _actors = [];", "List<Map<String, String>> _actors = [];\n  List<Map<String, String>> _directorsTmdb = [];")

# Add directors extraction in _fetchTmdbDetails
new_actors = """           _actors = casts.take(15).map((c) => {
              'id': c['id']?.toString() ?? '',
              'name': c['name']?.toString() ?? '',
              'character': c['character']?.toString() ?? '',
              'profile': c['profile_path'] != null ? 'https://image.tmdb.org/t/p/w200${c['profile_path']}' : '',
           }).toList();"""

new_directors = """
        if (details['credits'] != null && details['credits']['crew'] != null) {
           final crew = details['credits']['crew'] as List;
           _directorsTmdb = crew.where((c) => c['job'] == 'Director').map((c) => {
              'id': c['id']?.toString() ?? '',
              'name': c['name']?.toString() ?? '',
              'profile': c['profile_path'] != null ? 'https://image.tmdb.org/t/p/w200${c['profile_path']}' : '',
           }).toList();
        }
"""
content = content.replace(new_actors, new_actors + new_directors)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Directors state added")
