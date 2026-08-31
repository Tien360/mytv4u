import codecs

with codecs.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add to constructor
old_ctor = """  final int? season;
  final int? episode;
  final bool isLive;

  const PlayerScreen({
    super.key,
    required this.episodes,
    required this.currentEpisodeIndex,
    required this.movieName,
    this.imdbId,
    this.season,
    this.episode,
    this.isLive = false,
  });"""
new_ctor = """  final int? season;
  final int? episode;
  final bool isLive;
  final String? lazyPlaylistUrl;

  const PlayerScreen({
    super.key,
    required this.episodes,
    required this.currentEpisodeIndex,
    required this.movieName,
    this.imdbId,
    this.season,
    this.episode,
    this.isLive = false,
    this.lazyPlaylistUrl,
  });"""
code = code.replace(old_ctor, new_ctor)

with codecs.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)
print("Added lazyPlaylistUrl to constructor.")
