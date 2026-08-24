with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "episodeText = isSeries" in line:
        # replace the next 3 lines
        lines[i] = "      final String episodeText = isSeries\n"
        lines[i+1] = "          ? (_movie!.totalEpisodes.isNotEmpty && _movie!.totalEpisodes != '?' && _movie!.totalEpisodes != '0'\n"
        lines[i+2] = "              ? '${_movie!.episodes.first.items.length}/${_movie!.totalEpisodes} ${L10n.t('episodes') ?? 'Tập'}'\n"
        lines.insert(i+3, "              : '${_movie!.episodes.first.items.length} ${L10n.t('episodes')}')\n")
        lines[i+4] = "          : _movie!.currentEpisode;\n"
        break

# For directors
dir_start = -1
dir_end = -1
for i, line in enumerate(lines):
    if "if (_movie!.directors.isNotEmpty &&" in line:
        dir_start = i
    if dir_start != -1 and i > dir_start and "const SizedBox(height: 8)," in line:
        # Check if the next line is `],`
        if i + 1 < len(lines) and "]," in lines[i+1]:
            dir_end = i + 1
            break
if dir_start != -1 and dir_end != -1:
    lines = lines[:dir_start] + lines[dir_end+1:]
    print("Removed directors text")

# For next episode
next_start = -1
next_end = -1
for i, line in enumerate(lines):
    if "if (_tmdbDetails!['next_episode_to_air'] != null &&" in line:
        next_start = i
    if next_start != -1 and i > next_start and "]," in line:
        next_end = i
        break
if next_start != -1 and next_end != -1:
    lines = lines[:next_start] + ["""
                                            if (_tmdbDetails!['next_episode_to_air'] != null && _tmdbDetails!['next_episode_to_air']['air_date'] != null) ...[
                                              Builder(
                                                builder: (context) {
                                                  final airDateStr = _tmdbDetails!['next_episode_to_air']['air_date'];
                                                  String extraText = '';
                                                  try {
                                                    final airDate = DateTime.parse(airDateStr);
                                                    final now = DateTime.now();
                                                    final diff = airDate.difference(now).inDays;
                                                    if (diff > 0) {
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
                                            ],
"""] + lines[next_end+1:]
    print("Updated next episode logic")

# For overview
desc_start = -1
desc_end = -1
for i, line in enumerate(lines):
    if "SelectableText(" in line and i+1 < len(lines) and "_movie!.description.replaceAll(" in lines[i+1]:
        desc_start = i
    if desc_start != -1 and i > desc_start and ")," in line and i+1 < len(lines) and "textAlign: TextAlign.justify," in lines[i+1]:
        desc_end = i + 2
        break
if desc_start != -1 and desc_end != -1:
    lines = lines[:desc_start] + ["""
                                          Text(
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
                                          ),
"""] + lines[desc_end+1:]
    print("Updated description logic")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Done updates!")
