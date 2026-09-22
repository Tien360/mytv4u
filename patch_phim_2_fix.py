import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the body of fetchPremium
match = re.search(r'Future<void> fetchPremium\(\) async \{.*?(?=if \(enabledSources\.contains\(\'motchill\'\)\))', content, re.DOTALL)
if match:
    old_fetch = match.group(0)
    new_fetch = """Future<void> fetchPremium() async {
        bool slugMatches(String itemSlug) {
          if (slug == itemSlug) return true;
          final slugWords = slug.split('-');
          final itemWords = itemSlug.split('-');
          final overlap = itemWords
              .where((w) => slugWords.contains(w))
              .length;
          final minLen = [
            itemWords.length,
            slugWords.length,
          ].reduce((a, b) => a < b ? a : b);
          final minThreshold = [
            3,
            (minLen * 0.7).round(),
          ].reduce((a, b) => a > b ? a : b);
          return overlap >= minThreshold;
        }

        String querySlug = initialMovie?.sourceSlugs['premium'] ?? slug;
        Map<String, dynamic>? movieData;

        try {
          final data = await PremiumApi.getDetail(querySlug);
          if (data['movie'] != null) {
            movieData = data['movie'];
            
            final eps = movieData!['episodes'];
            final hasEmptyEps = eps == null || (eps is List && (eps.isEmpty || eps.every((srv) {
              final sd = srv['server_data'];
              return sd == null || (sd is List && sd.isEmpty);
            })));
            
            if (hasEmptyEps && querySlug.startsWith('premium-')) {
               String originalSlug = initialMovie?.sourceSlugs['premium_original'] ?? '';
               if (originalSlug.isEmpty || originalSlug.startsWith('premium-')) {
                  final movieName = (movieData!['name'] ?? movieData!['origin_name'] ?? '').toString();
                  final movieSlug = (movieData!['slug'] ?? '').toString();
                  if (movieSlug.isNotEmpty && !movieSlug.startsWith('premium-')) {
                     originalSlug = movieSlug;
                  } else if (movieName.isNotEmpty) {
                     final keyword = movieName.split(' ').take(5).join(' ');
                     try {
                        final searchData = await PremiumApi.searchMovies(keyword);
                        final items = (searchData['items'] as List?) ?? [];
                        for (var item in items) {
                           final itemSlug = (item['slug'] ?? '').toString();
                           if (itemSlug.isNotEmpty && !itemSlug.startsWith('premium-')) {
                              originalSlug = itemSlug;
                              break;
                           }
                        }
                     } catch (_) {}
                  }
               }
               
               if (originalSlug.isNotEmpty && originalSlug != querySlug && !originalSlug.startsWith('premium-')) {
                  try {
                     final data2 = await PremiumApi.getDetail(originalSlug);
                     if (data2['movie'] != null) movieData = data2['movie'];
                  } catch (_) {}
               }
            }
          }
        } catch (_) {}
        
        if (movieData == null && !querySlug.startsWith('premium-')) {
            final words = slug.split('-');
            if (words.length > 1) {
              final variations = [
                words[0],
                words.take(2).join('-'),
                words.skip(1).join('-'),
                if (words.length > 2) words.skip(2).join('-'),
                if (words.length > 3) words.skip(3).join('-'),
              ].where((v) => v.isNotEmpty && v != slug).toSet().toList();

              for (var v in variations) {
                try {
                  final data = await PremiumApi.getDetail(v);
                  if (data['movie'] != null) {
                    movieData = data['movie'];
                    break;
                  }
                } catch (_) {}
              }
            }
        }
        
        if (movieData == null && !querySlug.startsWith('premium-')) {
            final words = slug.split('-');
            final keywords = [
              if (initialMovie != null && initialMovie.originalName.isNotEmpty) initialMovie.originalName,
              if (initialMovie != null && initialMovie.name.isNotEmpty) initialMovie.name.replaceAll(RegExp(r'\\s+-\\s+.*'), ''),
              slug.replaceAll('-', ' '),
              words.isNotEmpty ? words[0] : '',
              words.length > 1 ? words.take(2).join(' ') : '',
            ].where((kw) => kw.length > 2).toSet().toList();
            
            for (var kw in keywords) {
              try {
                final searchData = await PremiumApi.searchMovies(kw);
                final items = (searchData['items'] as List?) ?? [];
                if (items.isNotEmpty) {
                  Map<String, dynamic>? bestMatch;
                  String bestSlug = '';
                  for (var item in items) {
                    final itemSlug = (item['slug'] ?? '').toString();
                    if (itemSlug.isNotEmpty && slugMatches(itemSlug)) {
                      bestMatch = item;
                      bestSlug = itemSlug;
                      break;
                    }
                    if (initialMovie != null && _isSimilarMovieGlobal(initialMovie, Movie.fromJson(item, defaultSource: 'premium'))) {
                      bestMatch = item;
                      bestSlug = itemSlug;
                      break;
                    }
                  }
                  
                  if (bestMatch != null) {
                    Map<String, dynamic>? detailData;
                    if (bestSlug.isNotEmpty && bestSlug != slug) {
                       try {
                         final detailRes = await PremiumApi.getDetail(bestSlug);
                         detailData = detailRes['movie'];
                       } catch (_) {}
                    }
                    if (detailData == null) {
                       final type = bestMatch['type'] == 'series' ? 'series' : 'movie';
                       final id = bestMatch['raw_payload'] ?? bestMatch['_id'];
                       if (id != null) {
                          try {
                             final detailRes = await PremiumApi.getDetail('premium-$type-$id');
                             detailData = detailRes['movie'];
                          } catch (_) {}
                          
                          if (detailData == null && bestSlug.isNotEmpty) {
                             try {
                                final detailRes = await PremiumApi.getDetail(bestSlug);
                                detailData = detailRes['movie'];
                             } catch (_) {}
                          }
                       }
                    }
                    if (detailData != null) {
                       movieData = detailData;
                       break;
                    }
                  }
                }
              } catch (_) {}
            }
        }
        
        if (movieData != null) {
            var m = Movie.fromJson(movieData as Map<String, dynamic>, defaultSource: 'premium').copyWith(quality: 'Premium');
            parsedMap[5] = m;
            
            List<EpisodeServer> premiumServers = [];
            final premEps = (movieData!['episodes'] as List?) ?? [];
            for (var srv in premEps) {
              final serverName = (srv['server_name'] ?? 'Premium Server').toString();
              List epItems = (srv['server_data'] is List) ? srv['server_data'] : ((srv['items'] is List) ? srv['items'] : []);
              final episodes = epItems.map((ep) {
                final link = (ep['link'] ?? ep['link_m3u8'] ?? '').toString();
                return Episode(
                  name: (ep['name'] ?? '').toString(),
                  slug: (ep['slug'] ?? '').toString(),
                  m3u8Url: link, // premium://...
                  embedUrl: (ep['link_embed'] ?? ep['embed'] ?? '').toString(),
                  filename: (ep['filename'] ?? '').toString(),
                );
              }).toList();
              premiumServers.add(EpisodeServer(serverName: serverName, items: episodes));
            }
            serversMap[5] = premiumServers;
            processAndEmit();
        }
    }
    
    futures.add(fetchPremium());
  }
      
  """
    
    content = content.replace(old_fetch, new_fetch)
    with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("phim_api.dart patched part 2 correctly")
else:
    print("Could not find fetchPremium in phim_api.dart")
