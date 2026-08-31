import re

with open('lib/api/film4knet_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

new_normalize = """static Movie normalize(Map<String, dynamic> item) {
    String title = '';
    String originalName = '';
    
    if (item['title'] is Map) {
      final titleObj = item['title'];
      title = titleObj['vi'] ?? titleObj['en'] ?? '';
      originalName = titleObj['en'] ?? title;
    } else if (item['title'] is String) {
      title = item['title'];
      originalName = item['originalName'] ?? item['original_name'] ?? title;
    }

    String poster = '';
    if (item['poster'] is Map) {
      final posterObj = item['poster'];
      poster = posterObj['vi'] ?? posterObj['en'] ?? '';
    } else if (item['poster'] is String) {
      poster = item['poster'];
    }

    final backdrop = item['backdrop'] ?? '';
    
    String overview = '';
    if (item['overview'] is Map) {
      final overviewObj = item['overview'];
      overview = overviewObj['vi'] ?? overviewObj['en'] ?? '';
    } else if (item['overview'] is String) {
      overview = item['overview'];
    }

    List<String> genresList = [];
    if (item['genres'] is Map) {
      final genresObj = item['genres'];
      final rawGenres = genresObj['vi'] ?? genresObj['en'] ?? [];
      if (rawGenres is List) {
        genresList = rawGenres.map((e) => e.toString()).toList();
      }
    } else if (item['genres'] is List) {
      genresList = (item['genres'] as List).map((e) => e.toString()).toList();
    }

    return Movie(
      name: title,
      originalName: originalName,
      slug: item['slug'] ?? '',
      type: item['mediaType'] == 'tv' ? 'series' : 'single',
      sourceSlugs: {'film4knet': item['slug'] ?? ''},
      thumbUrl: backdrop,
      posterUrl: poster,
      currentEpisode: '',
      quality: 'HD',
      language: 'Vietsub',
      year: (item['year'] ?? '').toString(),
      time: '',
      description: overview,
      genres: genresList,
      countries: [],
      directors: [],
      casts: [],
      episodes: [],
      source: 'film4knet',
    );
  }"""

# Find old normalize
start_idx = text.find("static Movie normalize(Map<String, dynamic> item) {")
end_idx = text.find("static Future<List<Movie>> getRecent", start_idx)

new_text = text[:start_idx] + new_normalize + "\n\n  " + text[end_idx:]

with open('lib/api/film4knet_api.dart', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Patched normalize")
