import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update episodeText logic
old_episodeText = "final String episodeText = isSeries\n          ? '${_movie!.episodes.first.items.length} ${L10n.t('episodes')}'\n          : _movie!.currentEpisode;"
new_episodeText = """final String episodeText = isSeries
          ? (_movie!.totalEpisodes.isNotEmpty && _movie!.totalEpisodes != '?' && _movie!.totalEpisodes != '0' 
              ? '${_movie!.episodes.first.items.length}/${_movie!.totalEpisodes} ${L10n.t('episodes') ?? 'Tập'}' 
              : '${_movie!.episodes.first.items.length} ${L10n.t('episodes')}')
          : _movie!.currentEpisode;"""

if old_episodeText in content:
    content = content.replace(old_episodeText, new_episodeText)
else:
    print("Could not find old_episodeText!")

# 2. Remove _movie!.directors block
dir_block_pattern = r"\s*if \(_movie!\.directors\.isNotEmpty &&[\s\S]*?_movie!\.directors\n\s*\.join\(\)\n\s*\.trim\(\)\n\s*\.isNotEmpty\) \.\.\.\[[\s\S]*?_buildRichText\([\s\S]*?L10n\.t\('directors'\),[\s\S]*?_movie!\.directors\.join\(\', \'\),[\s\S]*?\),[\s\S]*?const SizedBox\(height: 8\),[\s\S]*?\],"
if re.search(dir_block_pattern, content):
    content = re.sub(dir_block_pattern, "", content, count=1)
else:
    print("Could not find directors block to remove!")

# 3. Update next_episode_to_air
# Wait, let's find the existing block:
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
                                                      final phrases = [
                                                        ' (Còn $diff ngày nữa thôi!)',
                                                        ' (Chỉ $diff ngày nữa là cày!)',
                                                        ' (Sắp ra mắt sau $diff ngày!)',
                                                        ' (Ráng đợi $diff ngày nữa nhé!)'
                                                      ];
                                                      final random = DateTime.now().millisecondsSinceEpoch % phrases.length;
                                                      extraText = phrases[random];
                                                    } else if (diff == 0) {
                                                      extraText = ' (Chiếu trong hôm nay!)';
                                                    }
                                                  } catch (e) {}
                                                  return Column(
                                                    crossAxisAlignment: CrossAxisAlignment.start,
                                                    children: [
                                                      const SizedBox(height: 8),
                                                      _buildRichText('Tập tiếp theo: ', '$airDateStr$extraText'),
                                                    ],
                                                  );
                                                }
                                              )
                                            ],"""

if re.search(next_ep_pattern, content):
    content = re.sub(next_ep_pattern, new_next_ep, content, count=1)
else:
    print("Could not find next_episode pattern!")


# 4. Add "Nội dung phim" above _movie!.content and override with English from TMDB if en
content_pattern = r"(_movie!\.content\s*\?\?\s*'',\s*style:\s*const\s*TextStyle\(\s*color:\s*Colors\.white70,\s*fontSize:\s*14,\s*height:\s*1\.6,\s*\),\s*textAlign:\s*TextAlign\.justify,\s*\),)"
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

# I should replace the original SelectableText with the new one
full_content_pattern = r"SelectableText\(\s*_movie!\.content\s*\?\?\s*'',\s*style:\s*const\s*TextStyle\(\s*color:\s*Colors\.white70,\s*fontSize:\s*14,\s*height:\s*1\.6,\s*\),\s*textAlign:\s*TextAlign\.justify,\s*\),"
if re.search(full_content_pattern, content):
    content = re.sub(full_content_pattern, new_content_ui, content, count=1)
else:
    print("Could not find full_content_pattern!")


with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Done update!")
