import re

with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update _fetchAndMerge signature
text = text.replace(
    '''Future<List<Movie>> Function()? stremioFetcher,
  ) async {''',
    '''Future<List<Movie>> Function()? stremioFetcher,
    Future<List<Movie>> Function()? film4knetFetcher,
  ) async {'''
)

# 2. Update the futures array inside _fetchAndMerge
futures_replacement = '''enabledSources.contains('premium')
          ? _fetchPremiumSource(
              'https://dogtail.oxaliplatin.workers.dev/api/premium',
              'premium')
          : Future.value(<Movie>[]),
      enabledSources.contains('motchill')
          ? motchillFetcher()
          : Future.value(<Movie>[]),
      (enabledSources.contains('premium') && stremioFetcher != null)
          ? stremioFetcher()
          : Future.value(<Movie>[]),
      (enabledSources.contains('film4knet') && film4knetFetcher != null)
          ? film4knetFetcher()
          : Future.value(<Movie>[]),
    ];'''
text = re.sub(
    r\"enabledSources\.contains\('premium'\).*?\];\",
    futures_replacement,
    text,
    flags=re.DOTALL
)

# 3. Update the _mergeMovieItems call inside _fetchAndMerge
merge_call_replacement = '''return _mergeMovieItems(
      results[0] as List<Movie>,
      results[1] as List<Movie>,
      results[2] as List<Movie>,
      results[3] as List<Movie>,
      results[4] as List<Movie>,
      results[5] as List<Movie>,
      results[6] as List<Movie>,
      results[7] as List<Movie>,
      results[8] as List<Movie>,
      results[9] as List<Movie>,
    );'''
text = re.sub(
    r\"return _mergeMovieItems\(.*?results\[8\] as List<Movie>,\n    \);\",
    merge_call_replacement,
    text,
    flags=re.DOTALL
)

# 4. Update the _mergeMovieItems signature
text = text.replace(
    '''static List<Movie> _mergeMovieItems(
    List<Movie> listNguonC,
    List<Movie> listKKPhim,
    List<Movie> listOphim,
    List<Movie> listVSMov,
    List<Movie> listPhim4K,
    List<Movie> listFree1,
    List<Movie> listPremium,
    List<Movie> listMotchill,
    List<Movie> listStremio,
  ) {''',
    '''static List<Movie> _mergeMovieItems(
    List<Movie> listNguonC,
    List<Movie> listKKPhim,
    List<Movie> listOphim,
    List<Movie> listVSMov,
    List<Movie> listPhim4K,
    List<Movie> listFree1,
    List<Movie> listPremium,
    List<Movie> listMotchill,
    List<Movie> listStremio,
    List<Movie> listFilm4kNet,
  ) {'''
)

# 5. Update the list processing inside _mergeMovieItems
list_processing = '''for (var item in listNguonC) {
      addOrUpdate(item, 1);
    }
    for (var item in listKKPhim) {
      addOrUpdate(item, 2);
    }
    for (var item in listOphim) {
      addOrUpdate(item, 3);
    }
    for (var item in listVSMov) {
      addOrUpdate(item, 4);
    }
    for (var item in listPhim4K) {
      addOrUpdate(item, 5);
    }
    for (var item in listFree1) {
      addOrUpdate(item, 6);
    }
    for (var item in listPremium) {
      addOrUpdate(item, 7);
    }
    for (var item in listMotchill) {
      addOrUpdate(item, 8);
    }
    for (var item in listStremio) {
      addOrUpdate(item, 9);
    }
    for (var item in listFilm4kNet) {
      addOrUpdate(item, 10);
    }'''
text = re.sub(
    r\"for \(var item in listNguonC\).*?for \(var item in listStremio\) \{\n      addOrUpdate\(item, 9\);\n    \}\",
    list_processing,
    text,
    flags=re.DOTALL
)

# 6. Update the priority logic in _mergeMovieItems
priority_logic = '''int getPriority(Movie m) {
      if (m.sourceSlugs.containsKey('premium')) return 0;
      if (m.sourceSlugs.containsKey('film4knet')) return 1;
      if (m.sourceSlugs.containsKey('nguonc')) return 2;
      if (m.sourceSlugs.containsKey('kkphim')) return 3;
      if (m.sourceSlugs.containsKey('ophim')) return 4;
      if (m.sourceSlugs.containsKey('phim4k')) return 5;
      if (m.sourceSlugs.containsKey('free1')) return 6;
      if (m.sourceSlugs.containsKey('vsmov')) return 7;
      if (m.sourceSlugs.containsKey('motchill')) return 8;
      return 9;
    }'''
text = re.sub(
    r\"int getPriority\(Movie m\) \{.*?return 9;\n    \}\",
    priority_logic,
    text,
    flags=re.DOTALL
)

# 7. Update calls to _fetchAndMerge
text = text.replace(
    '''() => MotchillScraper.getRecent(page),
      null, // Don't fetch stremio for new updated because it takes too long/no pagination
    );''',
    '''() => MotchillScraper.getRecent(page),
      null, // Don't fetch stremio for new updated because it takes too long/no pagination
      () => Film4kNetApi.getRecent(page),
    );'''
)

text = text.replace(
    '''() => MotchillScraper.getByList(slug, page),
      null,
    );''',
    '''() => MotchillScraper.getByList(slug, page),
      null,
      null,
    );'''
)

text = text.replace(
    '''() => MotchillScraper.getByGenre(slug, page),
      null,
    );''',
    '''() => MotchillScraper.getByGenre(slug, page),
      null,
      null,
    );'''
)

text = text.replace(
    '''() => MotchillScraper.getByCountry(slug, page),
      null,
    );''',
    '''() => MotchillScraper.getByCountry(slug, page),
      null,
      null,
    );'''
)

text = text.replace(
    '''() => MotchillScraper.search(keyword),
      () => CinemetaApi.searchCinemeta(keyword),
    );''',
    '''() => MotchillScraper.search(keyword),
      () => CinemetaApi.searchCinemeta(keyword),
      () => Film4kNetApi.search(keyword),
    );'''
)

with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated phim_api.dart successfully!')
