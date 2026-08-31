import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

search_ctor = """class PlayerScreen extends StatefulWidget {
  final List<Episode> episodes;
  final int currentEpisodeIndex;
  final String movieName;
  final String? imdbId;
  final int? season;
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
new_ctor = """class PlayerScreen extends StatefulWidget {
  final List<Episode> episodes;
  final int currentEpisodeIndex;
  final String movieName;
  final String? imdbId;
  final int? season;
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

if search_ctor in content:
    content = content.replace(search_ctor, new_ctor)
    
search_init = """    _startHideControlsTimer();
    _loadSettingsAndInit();"""
new_init = """    _startHideControlsTimer();
    _loadSettingsAndInit();
    
    if (widget.lazyPlaylistUrl != null) {
      _startLazyPlaylistScraping(widget.lazyPlaylistUrl!);
    }"""
if "widget.lazyPlaylistUrl != null" not in content:
    content = content.replace(search_init, new_init)
    
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched lazyPlaylistUrl back in constructor")
