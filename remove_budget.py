with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Remove budget and revenue from Info section
content = content.replace("""                                            if (_tmdbDetails!['budget'] != null && _tmdbDetails!['budget'] > 0)
                                              _buildRichText('${L10n.t('budget') ?? 'Kinh phí'}: ', '\\$${_tmdbDetails!['budget'].toString().replaceAllMapped(RegExp(r'(\\d{1,3})(?=(\\d{3})+(?!\\d))'), (Match m) => '${m[1]},')}'),
                                            if (_tmdbDetails!['revenue'] != null && _tmdbDetails!['revenue'] > 0)
                                              _buildRichText('${L10n.t('revenue') ?? 'Doanh thu'}: ', '\\$${_tmdbDetails!['revenue'].toString().replaceAllMapped(RegExp(r'(\\d{1,3})(?=(\\d{3})+(?!\\d))'), (Match m) => '${m[1]},')}'),""", "")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Removed budget/revenue from info block")
