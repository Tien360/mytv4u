import re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

lists_insertion = """
                                // TMDB Collections & Recommendations
                                if (_tmdbDetails != null) ...[
                                  if (_tmdbDetails!['collection_details'] != null && _tmdbDetails!['collection_details']['parts'] != null && (_tmdbDetails!['collection_details']['parts'] as List).isNotEmpty)
                                    _buildTmdbHorizontalList(L10n.t('collection') ?? 'Bộ sưu tập', _tmdbDetails!['collection_details']['parts']),
                                    
                                  if (_tmdbDetails!['recommendations'] != null && _tmdbDetails!['recommendations']['results'] != null && (_tmdbDetails!['recommendations']['results'] as List).isNotEmpty)
                                    _buildTmdbHorizontalList(L10n.t('recommendations') ?? 'Có thể bạn cũng thích', _tmdbDetails!['recommendations']['results']),
                                    
                                  if ((_tmdbDetails!['recommendations'] == null || _tmdbDetails!['recommendations']['results'] == null || (_tmdbDetails!['recommendations']['results'] as List).isEmpty) && _tmdbDetails!['similar'] != null && _tmdbDetails!['similar']['results'] != null && (_tmdbDetails!['similar']['results'] as List).isNotEmpty)
                                    _buildTmdbHorizontalList(L10n.t('recommendations') ?? 'Có thể bạn cũng thích', _tmdbDetails!['similar']['results']),
                                ],
                                const SizedBox(height: 40),
"""

pattern = r"(// Badges\s*Wrap\()"
if re.search(pattern, content):
    content = re.sub(pattern, lambda m: lists_insertion + m.group(1), content)
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("Injected lists details")
else:
    print("Could not find target")
