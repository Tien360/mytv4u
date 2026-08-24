import re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

info_insertion = """
                                          const SizedBox(height: 16),
                                          if (_tmdbDetails != null) ...[
                                            if (_tmdbDetails!['status'] != null)
                                              _buildRichText(L10n.t('status') ?? 'Trạng thái', _tmdbDetails!['status'].toString()),
                                            if (_tmdbDetails!['production_companies'] != null && (_tmdbDetails!['production_companies'] as List).isNotEmpty)
                                              _buildRichText(L10n.t('production_companies') ?? 'Hãng sản xuất', (_tmdbDetails!['production_companies'] as List).map((c) => c['name']).join(', ')),
                                            if (_tmdbDetails!['budget'] != null && _tmdbDetails!['budget'] > 0)
                                              _buildRichText(L10n.t('budget') ?? 'Kinh phí', '\\$${_tmdbDetails!['budget'].toString().replaceAllMapped(RegExp(r'(\\d{1,3})(?=(\\d{3})+(?!\\d))'), (Match m) => '${m[1]},')}'),
                                            if (_tmdbDetails!['revenue'] != null && _tmdbDetails!['revenue'] > 0)
                                              _buildRichText(L10n.t('revenue') ?? 'Doanh thu', '\\$${_tmdbDetails!['revenue'].toString().replaceAllMapped(RegExp(r'(\\d{1,3})(?=(\\d{3})+(?!\\d))'), (Match m) => '${m[1]},')}'),
                                            if (_tmdbDetails!['imdb_id'] != null && _tmdbDetails!['imdb_id'].toString().isNotEmpty)
                                              _buildRichText(L10n.t('imdb_rating') ?? 'Điểm IMDb', 'ID: ${_tmdbDetails!['imdb_id']}'),
                                          ],
"""

pattern = r"(height:\s*1\.6,\s*\),\s*\),)"
if re.search(pattern, content):
    content = re.sub(pattern, lambda m: m.group(1) + info_insertion, content)
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("Injected info details")
else:
    print("Could not find target")
