import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

ep_pattern = r"final String episodeText = isSeries\s*\?\s*'\$\\{_movie!\.episodes\.first\.items\.length\\} \$\\{L10n\.t\('episodes'\)\\}'\s*:\s*_movie!\.currentEpisode;"

new_episodeText = """final String episodeText = isSeries
          ? (_movie!.totalEpisodes.isNotEmpty && _movie!.totalEpisodes != '?' && _movie!.totalEpisodes != '0' 
              ? '${_movie!.episodes.first.items.length}/${_movie!.totalEpisodes} ${L10n.t('episodes') ?? 'Tập'}' 
              : '${_movie!.episodes.first.items.length} ${L10n.t('episodes')}')
          : _movie!.currentEpisode;"""

if re.search(ep_pattern, content):
    content = re.sub(ep_pattern, new_episodeText, content, count=1)
    print("Fixed episodeText")
else:
    print("Could not find ep_pattern")

content_pattern = r"SelectableText\(\s*_movie!\.content\s*\?\?\s*'',\s*style:\s*const\s*TextStyle\(\s*color:\s*Colors\.white70,\s*fontSize:\s*14,\s*height:\s*1\.6,\s*\),\s*textAlign:\s*TextAlign\.justify,\s*\),"
new_content_ui = """Text(
                                L10n.t('overview') ?? 'Nội dung phim',
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 18,
                                ),
                              ),
                              const SizedBox(height: 12),
                              SelectableText(
                                (L10n.currentLang == 'en' && _tmdbDetails != null && _tmdbDetails!['overview'] != null && _tmdbDetails!['overview'].toString().isNotEmpty) 
                                    ? _tmdbDetails!['overview'] 
                                    : (_movie!.content ?? ''),
                                style: const TextStyle(
                                  color: Colors.white70,
                                  fontSize: 14,
                                  height: 1.6,
                                ),
                                textAlign: TextAlign.justify,
                              ),"""

# wait, did `SelectableText(` have an extra parameter?
# Let's check movie_detail_screen.dart for `_movie!.content ?? ''`
with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
