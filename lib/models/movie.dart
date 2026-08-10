import '../utils/l10n.dart';

class Movie {
  final String name;
  final String originalName;
  final String slug;
  final String type;
  final String? imdbId; // Added for OpenSubtitles and Torrentio TV Series
  final Map<String, String> sourceSlugs;
  final String thumbUrl;
  final String posterUrl;
  final String currentEpisode;
  final String quality;
  final String language;
  final String year;
  final String time;
  final String description;
  final List<String> genres;
  final List<String> countries;
  final List<String> directors;
  final List<String> casts;
  final List<EpisodeServer> episodes;
  final String source;

  String get displayName => (L10n.currentLang == 'en' && originalName.isNotEmpty) ? originalName : name;

  Movie({
    required this.name,
    required this.originalName,
    required this.slug,
    this.type = '',
    this.imdbId,
    this.sourceSlugs = const {},
    required this.thumbUrl,
    required this.posterUrl,
    required this.currentEpisode,
    required this.quality,
    required this.language,
    required this.year,
    required this.time,
    required this.description,
    required this.genres,
    required this.countries,
    required this.directors,
    required this.casts,
    required this.episodes,
    this.source = 'nguonc',
  });

  static String _extractYear(String raw) {
    if (raw.isEmpty) return '';
    // Handle date formats like "2026-07-13" → "2026"
    final match = RegExp(r'\d{4}').firstMatch(raw);
    return match?.group(0) ?? raw;
  }

  static List<String> _toStringList(dynamic value) {
    if (value == null) return [];
    if (value is List)
      return value
          .map<String>(
            (e) => e is Map ? (e['name'] ?? e.toString()) : e.toString(),
          )
          .toList();
    if (value is String && value.isNotEmpty)
      return value
          .split(',')
          .map((s) => s.trim())
          .where((s) => s.isNotEmpty)
          .toList();
    return [];
  }

  factory Movie.fromJson(
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
  }

  Movie copyWith({
    String? name,
    String? originalName,
    String? slug,
    String? type,
    String? imdbId,
    Map<String, String>? sourceSlugs,
    String? thumbUrl,
    String? posterUrl,
    String? currentEpisode,
    String? quality,
    String? language,
    String? year,
    String? time,
    String? description,
    String? source,
    List<String>? genres,
    List<String>? countries,
    List<String>? directors,
    List<String>? casts,
    List<EpisodeServer>? episodes,
  }) {
    return Movie(
      name: name ?? this.name,
      originalName: originalName ?? this.originalName,
      slug: slug ?? this.slug,
      type: type ?? this.type,
      imdbId: imdbId ?? this.imdbId,
      sourceSlugs: sourceSlugs ?? this.sourceSlugs,
      thumbUrl: thumbUrl ?? this.thumbUrl,
      posterUrl: posterUrl ?? this.posterUrl,
      currentEpisode: currentEpisode ?? this.currentEpisode,
      quality: quality ?? this.quality,
      language: language ?? this.language,
      year: year ?? this.year,
      time: time ?? this.time,
      description: description ?? this.description,
      genres: genres ?? this.genres,
      countries: countries ?? this.countries,
      directors: directors ?? this.directors,
      casts: casts ?? this.casts,
      episodes: episodes ?? this.episodes,
      source: source ?? this.source,
    );
  }
}

class EpisodeServer {
  final String serverName;
  final List<Episode> items;

  EpisodeServer({required this.serverName, required this.items});
}

class Episode {
  final String name;
  final String slug;
  final String m3u8Url;
  final String embedUrl;

  Episode({
    required this.name,
    required this.slug,
    required this.m3u8Url,
    required this.embedUrl,
  });
}
