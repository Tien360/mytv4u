with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

old_episodeText = """      final String episodeText = isSeries
          ? '${_movie!.episodes.first.items.length} ${L10n.t('episodes')}'
          : _movie!.currentEpisode;"""

new_episodeText = """      final String episodeText = isSeries
          ? (_movie!.totalEpisodes.isNotEmpty && _movie!.totalEpisodes != '?' 
              ? '${_movie!.episodes.first.items.length}/${_movie!.totalEpisodes} ${L10n.t('episodes') ?? 'Tập'}' 
              : '${_movie!.episodes.first.items.length} ${L10n.t('episodes')}')
          : _movie!.currentEpisode;"""

content = content.replace(old_episodeText, new_episodeText)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated episodeText")
