import re

with open("lib/models/movie.dart", "r", encoding="utf-8") as f:
    content = f.read()

old_code = """  factory Movie.fromJson(
    Map<String, dynamic> json, {
    String defaultSource = 'nguonc',
  }) {
    return Movie(
      name: json['name'] ?? '',
      originalName: json['original_name'] ?? json['origin_name'] ?? '',
      slug: json['slug'] ?? '',
      type: json['type'] ?? '',
      imdbId: null,
      sourceSlugs: {defaultSource: json['slug'] ?? ''},
      thumbUrl: json['thumb_url'] ?? '',
      posterUrl: json['poster_url'] ?? '',
      currentEpisode: json['current_episode'] ?? json['episode_current'] ?? '',
      quality: json['quality'] ?? '',
      language: json['language'] ?? json['lang'] ?? '',
      year: _extractYear(json['year']?.toString() ?? ''),
      time: json['time']?.toString() ?? '',
      description: (json['description'] ?? json['content'] ?? '')
          .toString()
          .replaceAll('Xem thêm', '')
          .trim(),
      genres: _toStringList(json['genres'] ?? json['category']),
      countries: _toStringList(json['countries'] ?? json['country']),
      directors: _toStringList(json['directors'] ?? json['director']),
      casts: _toStringList(json['casts'] ?? json['actor']),
      episodes: [],
      source: json['source'] ?? defaultSource,
    );
  }"""

new_code = """  factory Movie.fromJson(
    Map<String, dynamic> json, {
    String defaultSource = 'nguonc',
  }) {
    String parsedName = json['name'] ?? '';
    String parsedOriginalName = json['original_name'] ?? json['origin_name'] ?? '';
    String parsedYear = _extractYear(json['year']?.toString() ?? '');

    // Premium source specific name parsing logic
    // Pattern: "Vietnamese Name (Year) English Name"
    final regex = RegExp(r'^(.*?)\\s*\\((\\d{4})\\)\\s*(.*)$');
    final match = regex.firstMatch(parsedName);
    if (match != null) {
      parsedName = match.group(1)?.trim() ?? parsedName;
      String extractedYear = match.group(2) ?? '';
      if (parsedYear.isEmpty && extractedYear.isNotEmpty) {
        parsedYear = extractedYear;
      }
      String extractedOriginalName = match.group(3)?.trim() ?? '';
      if (extractedOriginalName.isNotEmpty) {
        parsedOriginalName = extractedOriginalName;
      }
    }

    return Movie(
      name: parsedName,
      originalName: parsedOriginalName,
      slug: json['slug'] ?? '',
      type: json['type'] ?? '',
      imdbId: null,
      sourceSlugs: {defaultSource: json['slug'] ?? ''},
      thumbUrl: json['thumb_url'] ?? '',
      posterUrl: json['poster_url'] ?? '',
      currentEpisode: json['current_episode'] ?? json['episode_current'] ?? '',
      quality: json['quality'] ?? '',
      language: json['language'] ?? json['lang'] ?? '',
      year: parsedYear,
      time: json['time']?.toString() ?? '',
      description: (json['description'] ?? json['content'] ?? '')
          .toString()
          .replaceAll('Xem thêm', '')
          .trim(),
      genres: _toStringList(json['genres'] ?? json['category']),
      countries: _toStringList(json['countries'] ?? json['country']),
      directors: _toStringList(json['directors'] ?? json['director']),
      casts: _toStringList(json['casts'] ?? json['actor']),
      episodes: [],
      source: json['source'] ?? defaultSource,
    );
  }"""

content = content.replace(old_code, new_code)
with open("lib/models/movie.dart", "w", encoding="utf-8") as f:
    f.write(content)
