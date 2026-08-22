import re

with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

film4k_block = '''if (enabledSources.contains('film4knet')) {
          final querySlug = initialMovie?.sourceSlugs['film4knet'] ?? slug;
          final guessedSlug = (initialMovie != null && initialMovie.originalName.isNotEmpty)
              ? _slugify(initialMovie.originalName)
              : querySlug;
          
          void handleFilm4kResponse(Movie? fetchedMovie) {
             if (fetchedMovie != null && _isSimilarMovieGlobal(initialMovie, fetchedMovie)) {
                parsedMap[10] = fetchedMovie;
                serversMap[10] = fetchedMovie.episodes;
                processAndEmit();
             }
          }

          futures.add(
            Film4kNetApi.getDetail(querySlug).then((fetchedMovie) {
              if (fetchedMovie != null) {
                handleFilm4kResponse(fetchedMovie);
              } else if (guessedSlug != querySlug && guessedSlug.isNotEmpty) {
                Film4kNetApi.getDetail(guessedSlug).then(handleFilm4kResponse).catchError((_) {});
              }
            }).catchError((_) {
               if (guessedSlug != querySlug && guessedSlug.isNotEmpty) {
                  Film4kNetApi.getDetail(guessedSlug).then(handleFilm4kResponse).catchError((_) {});
               }
            }),
          );
        }'''

new_film4k_block = '''if (enabledSources.contains('film4knet')) {
          final querySlug = initialMovie?.sourceSlugs['film4knet'] ?? slug;
          final guessedSlug = (initialMovie != null && initialMovie.originalName.isNotEmpty)
              ? _slugify(initialMovie.originalName)
              : querySlug;
          
          bool handleFilm4kResponse(Movie? fetchedMovie) {
             if (fetchedMovie != null && _isSimilarMovieGlobal(initialMovie, fetchedMovie)) {
                parsedMap[10] = fetchedMovie;
                serversMap[10] = fetchedMovie.episodes;
                processAndEmit();
                return true;
             }
             return false;
          }

          futures.add(
            Film4kNetApi.getDetail(querySlug).then((fetchedMovie) {
              bool success = handleFilm4kResponse(fetchedMovie);
              if (!success && guessedSlug != querySlug && guessedSlug.isNotEmpty) {
                Film4kNetApi.getDetail(guessedSlug).then(handleFilm4kResponse).catchError((_) {});
              }
            }).catchError((_) {
               if (guessedSlug != querySlug && guessedSlug.isNotEmpty) {
                  Film4kNetApi.getDetail(guessedSlug).then(handleFilm4kResponse).catchError((_) {});
               }
            }),
          );
        }'''

if film4k_block in text:
    text = text.replace(film4k_block, new_film4k_block)
    with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Done")
else:
    print("Not found")
