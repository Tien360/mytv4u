import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update episodeText logic
ep_pattern = r"final String episodeText = isSeries\n\s*\?\s*'[^']*?'\n\s*:\s*_movie!\.currentEpisode;"

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

# 2. Remove _movie!.directors block
# Search for `if (_movie!.directors.isNotEmpty &&` and the end of the `...[` block which is `const SizedBox(height: 8),\n                                          ],`
dir_pattern = r"\s*if \(_movie!\.directors\.isNotEmpty &&[\s\S]*?const SizedBox\(height: 8\),\s*\],"
if re.search(dir_pattern, content):
    content = re.sub(dir_pattern, "", content, count=1)
    print("Removed directors block")
else:
    print("Could not find dir_pattern")

# 3. Update next_episode_to_air
next_ep_pattern = r"\s*if \(_tmdbDetails!\['next_episode_to_air'\] != null &&\s*_tmdbDetails!\['next_episode_to_air'\]\['air_date'\] != null\) \.\.\.\[[\s\S]*?_buildRichText\('Tập tiếp theo: ',[\s\S]*?_tmdbDetails!\['next_episode_to_air'\]\['air_date'\]\),[\s\S]*?\],"

new_next_ep = """
                                            if (_tmdbDetails!['next_episode_to_air'] != null && 
_tmdbDetails!['next_episode_to_air']['air_date'] != null) ...[
                                              Builder(
                                                builder: (context) {
                                                  final airDateStr = _tmdbDetails!['next_episode_to_air']['air_date'];
                                                  String extraText = '';
                                                  try {
                                                    final airDate = DateTime.parse(airDateStr);
                                                    final now = DateTime.now();
                                                    final diff = airDate.difference(now).inDays;
                                                    if (diff > 0) {
                                                      final title = L10n.t('next_episode') ?? 'Tập tiếp theo: ';
                                                      final extraMap = {
                                                        'en': [
                                                          ' ($diff days left!)',
                                                          ' (Only $diff days!)',
                                                          ' (Coming in $diff days!)'
                                                        ],
                                                        'vi': [
                                                          ' (Còn $diff ngày nữa thôi!)',
                                                          ' (Chỉ $diff ngày nữa là cày!)',
                                                          ' (Sắp ra mắt sau $diff ngày!)',
                                                          ' (Ráng đợi $diff ngày nữa nhé!)'
                                                        ]
                                                      };
                                                      final phrases = extraMap[L10n.currentLang] ?? extraMap['vi']!;
                                                      final random = DateTime.now().millisecondsSinceEpoch % phrases.length;
                                                      extraText = phrases[random];
                                                    } else if (diff == 0) {
                                                      extraText = (L10n.currentLang == 'en') ? ' (Airing today!)' : ' (Chiếu trong hôm nay!)';
                                                    } else {
                                                       extraText = (L10n.currentLang == 'en') ? ' (Aired)' : ' (Đã lên sóng)';
                                                    }
                                                  } catch (e) {}
                                                  return Column(
                                                    crossAxisAlignment: CrossAxisAlignment.start,
                                                    children: [
                                                      const SizedBox(height: 8),
                                                      _buildRichText(L10n.t('next_episode') ?? 'Tập tiếp theo: ', '$airDateStr$extraText'),
                                                    ],
                                                  );
                                                }
                                              )
                                            ],"""

if re.search(next_ep_pattern, content):
    content = re.sub(next_ep_pattern, new_next_ep, content, count=1)
    print("Updated next episode logic")
else:
    print("Could not find next_ep_pattern")


# 4. Add "Nội dung phim" above _movie!.description and override with English from TMDB if en
desc_pattern = r"SelectableText\(\s*_movie!\.description\.replaceAll\([\s\S]*?TextAlign\.justify,\s*\),"
new_desc_ui = """Text(
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
                                                : _movie!.description.replaceAll(
                                                    RegExp(r'<[^>]*>|&[^;]+;'),
                                                    '',
                                                  ),
                                            style: const TextStyle(
                                              color: Colors.white70,
                                              fontSize: 14,
                                              height: 1.6,
                                            ),
                                            textAlign: TextAlign.justify,
                                          ),"""

if re.search(desc_pattern, content):
    content = re.sub(desc_pattern, new_desc_ui, content, count=1)
    print("Updated description logic")
else:
    print("Could not find desc_pattern")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Done updates!")
