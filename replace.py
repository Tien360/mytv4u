import os

file_path = "t:/Project/Phim/mytv4u_flutter/lib/api/phim_api.dart"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# We need to replace `fetchMovieDetailStream`
start_str = "static Stream<Movie> fetchMovieDetailStream(String slug) {"
end_str = "    return controller.stream;\n  }"

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx) + len(end_str)

new_method = """  static Stream<Movie> fetchMovieDetailStream(String slug) {
    final controller = StreamController<Movie>();
    final Map<int, Movie> parsedMap = {};
    final Map<int, List<EpisodeServer>> serversMap = {};

    void processAndEmit() {
      if (parsedMap.isEmpty) return;
      
      final order = [6, 3, 7, 1, 0, 2, 4, 5]; 
      
      List<Movie> orderedMovies = [];
      List<EpisodeServer> allServers = [];
      
      for (var idx in order) {
        if (parsedMap.containsKey(idx)) orderedMovies.add(parsedMap[idx]!);
      }
      
      for (var idx in order) {
        if (serversMap.containsKey(idx)) allServers.addAll(serversMap[idx]!);
      }

      if (orderedMovies.isEmpty) return;

      Movie merged = orderedMovies.first;
      for (int i = 1; i < orderedMovies.length; i++) {
        var item = orderedMovies[i];
        bool isPremium = item.source == 'premium';
        merged = merged.copyWith(
          thumbUrl: item.thumbUrl.isNotEmpty ? item.thumbUrl : merged.thumbUrl,
          posterUrl: item.posterUrl.isNotEmpty ? item.posterUrl : merged.posterUrl,
          currentEpisode: (item.currentEpisode.isNotEmpty && item.currentEpisode != 'Đang cập nhật') ? item.currentEpisode : merged.currentEpisode,
          quality: (item.quality.isNotEmpty && item.quality != 'FHD' && item.quality != 'N/A') ? item.quality : merged.quality,
          time: (item.time.isNotEmpty && item.time != 'N/A') ? item.time : merged.time,
          language: (item.language.isNotEmpty && item.language != 'Vietsub' && item.language != 'N/A') ? item.language : merged.language,
          description: (isPremium && merged.description.isNotEmpty) ? merged.description : (item.description.isNotEmpty ? item.description : merged.description),
          year: item.year.isNotEmpty ? item.year : merged.year,
          genres: (isPremium && merged.genres.isNotEmpty) ? merged.genres : (item.genres.isNotEmpty ? item.genres : merged.genres),
          countries: item.countries.isNotEmpty ? item.countries : merged.countries,
          directors: item.directors.isNotEmpty ? item.directors : merged.directors,
          casts: item.casts.isNotEmpty ? item.casts : merged.casts,
          source: merged.source != item.source ? 'mixed' : merged.source,
        );
      }

      merged = merged.copyWith(
        episodes: allServers.where((server) => server.items.any((ep) => ep.m3u8Url.isNotEmpty || ep.embedUrl.isNotEmpty)).toList(),
      );
      
      controller.add(merged);
    }

    SharedPreferences.getInstance().then((prefs) {
      final enabledSources = prefs.getStringList('enabled_sources') ?? ['premium', 'nguonc', 'ophim', 'kkphim', 'vsmov', 'phim4k', 'free1', 'motchill'];
      final timeout = const Duration(seconds: 5);
      final List<Future> futures = [];

      if (enabledSources.contains('nguonc')) {
        futures.add(http.get(Uri.parse('$nguoncUrl/film/$slug')).timeout(timeout).then((res) {
          if (res.statusCode == 200) {
            final data = json.decode(res.body);
            final movieData = data['movie'] ?? data['item'];
            if (movieData != null) {
              parsedMap[0] = _normalizeNguonC(movieData);
              serversMap[0] = _parseEpisodes((movieData['episodes'] as List?) ?? [], 'NguonC');
              processAndEmit();
            }
          }
        }).catchError((_) {}));
      }

      if (enabledSources.contains('kkphim')) {
        futures.add(http.get(Uri.parse('$kkphimUrl/phim/$slug')).timeout(timeout).then((res) {
          if (res.statusCode == 200) {
            final data = json.decode(res.body);
            final movieData = (data['data'] != null) ? (data['data']['item'] ?? data['data']['movie']) : (data['movie'] ?? data['item']);
            if (movieData != null) {
              parsedMap[1] = _normalizeKKPhim(movieData);
              final epsList = ((data['data'] != null ? data['data']['item']?['episodes'] : null) ?? data['episodes'] ?? data['episode'] ?? movieData['episodes'] ?? movieData['episode']) as List? ?? [];
              serversMap[1] = _parseEpisodes(epsList, 'KKPhim');
              processAndEmit();
            }
          }
        }).catchError((_) {}));
      }

      if (enabledSources.contains('ophim')) {
        futures.add(http.get(Uri.parse('$ophimUrl/phim/$slug')).timeout(timeout).then((res) {
          if (res.statusCode == 200) {
            final data = json.decode(res.body);
            final movieData = (data['data'] != null) ? (data['data']['item'] ?? data['data']['movie']) : (data['movie'] ?? data['item']);
            if (movieData != null) {
              parsedMap[7] = _normalizeOphim(movieData);
              final epsList = ((data['data'] != null ? data['data']['item']?['episodes'] : null) ?? data['episodes'] ?? data['episode'] ?? movieData['episodes'] ?? movieData['episode']) as List? ?? [];
              serversMap[7] = _parseEpisodes(epsList, 'Ophim');
              processAndEmit();
            }
          }
        }).catchError((_) {}));
      }

      if (enabledSources.contains('phim4k')) {
        futures.add(http.get(Uri.parse('$phim4kUrl/film/$slug')).timeout(timeout).then((res) {
          if (res.statusCode == 200) {
            final data = json.decode(res.body);
            final movieData = data['movie'] ?? data['item'];
            if (movieData != null) {
              parsedMap[2] = _normalizePhim4K(movieData);
              serversMap[2] = _parseEpisodes((movieData['episodes'] as List?) ?? [], 'Free2');
              processAndEmit();
            }
          }
        }).catchError((_) {}));
      }

      if (enabledSources.contains('vsmov')) {
        futures.add(http.get(Uri.parse('$vsmovUrl/phim/$slug')).timeout(timeout).then((res) {
          if (res.statusCode == 200) {
            final data = json.decode(res.body);
            final movieData = data['movie'] ?? data['item'];
            if (movieData != null) {
              parsedMap[3] = _normalizeVSMov(movieData);
              serversMap[3] = _parseEpisodes((movieData['episodes'] as List?) ?? [], 'VSMov');
              processAndEmit();
            }
          }
        }).catchError((_) {}));
      }

      if (enabledSources.contains('free1')) {
        futures.add(http.get(Uri.parse('$free1Url/phim/$slug')).timeout(timeout).then((res) {
          if (res.statusCode == 200) {
            final data = json.decode(res.body);
            final movieData = (data['data'] != null) ? data['data']['item'] : (data['movie'] ?? data['item']);
            if (movieData != null) {
              parsedMap[4] = _normalizeFree1(movieData);
              serversMap[4] = _parseEpisodes((movieData['episodes'] as List?) ?? [], 'Free1');
              processAndEmit();
            }
          }
        }).catchError((_) {}));
      }

      if (enabledSources.contains('premium')) {
        futures.add(http.get(Uri.parse('https://dogtail.oxaliplatin.workers.dev/api/premium/detail/$slug')).timeout(timeout).then((res) {
          if (res.statusCode == 200) {
            final data = json.decode(res.body);
            final movieData = data['movie'] ?? data['item'];
            if (movieData != null) {
              var m = Movie.fromJson(movieData as Map<String, dynamic>, defaultSource: 'premium').copyWith(quality: 'Premium');
              parsedMap[5] = m;
              
              List<EpisodeServer> premiumServers = [];
              final premEps = (movieData['episodes'] as List?) ?? [];
              for (var srv in premEps) {
                final serverName = srv['server_name'] ?? 'Premium Server';
                List epItems = (srv['server_data'] is List) ? srv['server_data'] : ((srv['items'] is List) ? srv['items'] : []);
                final episodes = epItems.map((ep) {
                  return Episode(
                    name: ep['name'] ?? '',
                    slug: ep['slug'] ?? '',
                    m3u8Url: ep['link'] ?? ep['link_m3u8'] ?? '',
                    embedUrl: ep['link_embed'] ?? ep['embed'] ?? '',
                  );
                }).toList();
                premiumServers.add(EpisodeServer(serverName: serverName, items: episodes));
              }
              serversMap[5] = premiumServers;
              processAndEmit();
            }
          }
        }).catchError((_) {}));
      }

      if (enabledSources.contains('motchill')) {
        futures.add(MotchillScraper.getDetail(slug).timeout(timeout).then((movie) {
          if (movie != null) {
            parsedMap[6] = movie;
            serversMap[6] = movie.episodes;
            processAndEmit();
          }
        }).catchError((_) {}));
      }

      Future.wait(futures).then((_) {
        processAndEmit();
        controller.close();
      }).catchError((_) {
        controller.close();
      });
    });

    return controller.stream;
  }"""

new_content = content[:start_idx] + new_method + content[end_idx:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Replaced fetchMovieDetailStream successfully.")
