import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update the episode badge
old_badge = """                          if (_movie!.episodes.isNotEmpty &&
                              _movie!.episodes.first.items.isNotEmpty)
                            _buildBadge(
                              Icons.layers,
                              '${_movie!.episodes.first.items.length} episodes',
                              Colors.orange,
                            ),"""
new_badge = """                          if (_movie!.episodes.isNotEmpty &&
                              _movie!.episodes.first.items.isNotEmpty)
                            _buildBadge(
                              Icons.layers,
                              _movie!.totalEpisodes.isNotEmpty && _movie!.totalEpisodes != '?'
                                  ? '${_movie!.episodes.first.items.length}/${_movie!.totalEpisodes} ${L10n.t('episodes') ?? 'Tập'}'
                                  : '${_movie!.episodes.first.items.length} ${L10n.t('episodes') ?? 'Tập'}',
                              Colors.orange,
                            ),"""
if old_badge in content:
    content = content.replace(old_badge, new_badge)

# 2. Remove the episode text from the info block that I added previously
old_info_ep = """                                            if (_movie!.type == 'series' || _movie!.type == 'hoathinh' || _movie!.type == 'tvshows') ...[
                                              const SizedBox(height: 8),
                                              _buildRichText(
                                                '${L10n.t('episodes') ?? 'Số tập'}: ',
                                                _movie!.totalEpisodes.isNotEmpty && _movie!.totalEpisodes != '?'
                                                    ? '${_movie!.episodes.isNotEmpty ? _movie!.episodes.first.items.length : 0}/${_movie!.totalEpisodes}'
                                                    : '${_movie!.episodes.isNotEmpty ? _movie!.episodes.first.items.length : 0}',
                                              ),
                                            ],"""
content = content.replace(old_info_ep, "")

# 3. Add Next Episode Air Date + Budget/Revenue to Info column
new_info_additions = """
                                            if (_tmdbDetails!['next_episode_to_air'] != null && _tmdbDetails!['next_episode_to_air']['air_date'] != null) ...[
                                              const SizedBox(height: 8),
                                              _buildRichText('Tập tiếp theo: ', _tmdbDetails!['next_episode_to_air']['air_date']),
                                            ],
                                            if (_tmdbDetails!['budget'] != null && _tmdbDetails!['budget'] > 0 && _tmdbDetails!['revenue'] != null && _tmdbDetails!['revenue'] > 0) ...[
                                              const SizedBox(height: 8),
                                              _buildRichText('Kinh phí: ', '\\$${(_tmdbDetails!['budget'] / 1000000).toStringAsFixed(1)}M'),
                                              const SizedBox(height: 8),
                                              _buildRichText('Doanh thu: ', '\\$${(_tmdbDetails!['revenue'] / 1000000).toStringAsFixed(1)}M'),
                                            ],
"""
# Insert after "Hãng sản xuất" block
pattern = r"(\.where\(\(c\) => c\['logo_path'\] != null\).*?\.toList\(\),\s*\),\s*const SizedBox\(height: 8\),\s*\]\,)"
if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, lambda m: m.group(1) + new_info_additions, content, count=1, flags=re.DOTALL)

# 4. Remove the buggy finance UI from the right column
pattern2 = r"if \(_tmdbDetails != null && _tmdbDetails!\['budget'\] != null && \s*_tmdbDetails!\['budget'\] > 0 && _tmdbDetails!\['revenue'\] != null && _tmdbDetails!\['revenue'\] > 0\) \.\.\.\[.*?\]\,\s*"
content = re.sub(pattern2, "", content, flags=re.DOTALL)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated movie_detail_screen.dart")
