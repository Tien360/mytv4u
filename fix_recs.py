with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Replace the usages
text = text.replace("_buildTmdbHorizontalList(L10n.t('collection') ?? 'Bộ sưu tập', _tmdbDetails!['collection_details']['parts']),", 
                    "TmdbHorizontalList(title: L10n.t('collection') ?? 'Bộ sưu tập', items: _tmdbDetails!['collection_details']['parts'], onSearchAndPlay: _searchAndPlayTmdbMovie),")
text = text.replace("_buildTmdbHorizontalList(L10n.t('recommendations') ?? 'Có thể bạn cũng thích', _tmdbDetails!['recommendations']['results']),",
                    "TmdbHorizontalList(title: L10n.t('recommendations') ?? 'Có thể bạn cũng thích', items: _tmdbDetails!['recommendations']['results'], onSearchAndPlay: _searchAndPlayTmdbMovie),")
text = text.replace("_buildTmdbHorizontalList(L10n.t('recommendations') ?? 'Có thể bạn cũng thích', _tmdbDetails!['similar']['results']),",
                    "TmdbHorizontalList(title: L10n.t('recommendations') ?? 'Có thể bạn cũng thích', items: _tmdbDetails!['similar']['results'], onSearchAndPlay: _searchAndPlayTmdbMovie),")

# 2. Append the class
with open("TmdbHorizontalList.dart", "rb") as f:
    widget_code = f.read().replace(b'\xef\xbb\xbf', b'').decode('utf-8')

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text + "\n" + widget_code)
print("Updated movie_detail_screen.dart for recommendations arrows!")
