
with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad_block = '''        if (enabledSources.contains('film4knet')) {
          final querySlug = initialMovie?.sourceSlugs['film4knet'] ?? slug;
          futures.add(
            Film4kNetApi.getDetail(querySlug).then((fetchedMovie) {
              if (fetchedMovie != null &&
                  _isSimilarMovieGlobal(initialMovie, fetchedMovie)) {
                parsedMap[10] = fetchedMovie;
                serversMap[10] = fetchedMovie.episodes;
                processAndEmit();
              }
            }),
          );
        }'''

if bad_block in text:
    text = text.replace(bad_block + '\n  \n        final List<Future> futures = [];', '        final List<Future> futures = [];\n\n' + bad_block)
    with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed futures.add position')
else:
    print('Block not found')

