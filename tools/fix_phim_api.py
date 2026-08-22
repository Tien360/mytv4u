
import sys
with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('import ''cinemeta_api.dart'';', 'import ''cinemeta_api.dart'';\nimport ''film4knet_api.dart'';')

text = text.replace(
'''      Future<List<Movie>> Function() motchillFetcher,''',
'''      Future<List<Movie>> Function() film4kNetFetcher,
      Future<List<Movie>> Function() motchillFetcher,''')

text = text.replace(
'''      mergeList(itemsFree1);''',
'''      mergeList(itemsFree1);
      mergeList(itemsFilm4kNet);''')

text = text.replace(
'''      List<Movie> itemsMotchill,''',
'''      List<Movie> itemsFilm4kNet,
      List<Movie> itemsMotchill,''')

text = text.replace(
'''        if (m.sourceSlugs.containsKey('free1')) return 6;''',
'''        if (m.sourceSlugs.containsKey('film4knet')) return 6;
        if (m.sourceSlugs.containsKey('free1')) return 7;''')

text = text.replace(
'''        if (m.sourceSlugs.containsKey('vsmov')) return 7;''',
'''        if (m.sourceSlugs.containsKey('vsmov')) return 8;''')

text = text.replace(
'''        if (m.sourceSlugs.containsKey('motchill')) return 8;''',
'''        if (m.sourceSlugs.containsKey('motchill')) return 9;''')

text = text.replace(
'''        return 9;''',
'''        return 10;''')

text = text.replace(
'''        enabledSources.contains('motchill')
            ? motchillFetcher()
            : Future.value(<Movie>[]),''',
'''        enabledSources.contains('film4knet')
            ? film4kNetFetcher()
            : Future.value(<Movie>[]),
        enabledSources.contains('motchill')
            ? motchillFetcher()
            : Future.value(<Movie>[]),''')

text = text.replace(
'''        () => MotchillScraper.getRecent(page),''',
'''        () => Film4kNetApi.getRecent(page),
        () => MotchillScraper.getRecent(page),''')

text = text.replace(
'''        () => MotchillScraper.getByList(slug, page),''',
'''        () => Future.value(<Movie>[]),
        () => MotchillScraper.getByList(slug, page),''')

text = text.replace(
'''        () => MotchillScraper.getByGenre(slug, page),''',
'''        () => Future.value(<Movie>[]),
        () => MotchillScraper.getByGenre(slug, page),''')

text = text.replace(
'''        () => MotchillScraper.getByCountry(slug, page),''',
'''        () => Future.value(<Movie>[]),
        () => MotchillScraper.getByCountry(slug, page),''')

text = text.replace(
'''        () => MotchillScraper.search(keyword),''',
'''        () => Film4kNetApi.search(keyword),
        () => MotchillScraper.search(keyword),''')

detail_logic = '''
      if (enabledSources.contains('film4knet')) {
        final querySlug = initialMovie?.sourceSlugs['film4knet'] ?? slug;
        futures.add(
          Film4kNetApi.getDetail(querySlug).then((fetchedMovie) {
            if (fetchedMovie != null && _isSimilarMovieGlobal(initialMovie, fetchedMovie)) {
              parsedMap[10] = fetchedMovie;
              serversMap[10] = fetchedMovie.episodes;
              processAndEmit();
            }
          })
        );
      }
'''
text = text.replace('final timeout = const Duration(seconds: 5);', 'final timeout = const Duration(seconds: 5);\n' + detail_logic)

with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done')

