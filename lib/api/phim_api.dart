import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:youtube_explode_dart/youtube_explode_dart.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/movie.dart';
import 'motchill_scraper.dart';
import 'film4knet_api.dart';
import 'torrentio_api.dart';
import 'cinemeta_api.dart';

class PhimApi {
  static const String nguoncUrl = 'https://phim.nguonc.com/api';
  static const String kkphimUrl = 'https://phimapi.com/v1/api';
  static const String ophimUrl = 'https://ophim1.com/v1/api';
  static const String vsmovUrl = 'https://vsmov.com/api';
  static const String phim4kUrl = 'https://free2.phim4k.lol/api';
  static const String free1Url = 'https://free1.phim4k.lol/v1/api';
  static const String premiumUrl =
      'https://dogtail.oxaliplatin.workers.dev/api/premium';
  static const String free1List = 'https://free1.phim4k.lol/danh-sach';

  // --- Normalization functions ---
  static Movie _normalizeNguonC(Map<String, dynamic> item) {
    return Movie.fromJson(item, defaultSource: 'nguonc');
  }

  static Movie _normalizeKKPhim(Map<String, dynamic> item) {
    var m = Movie.fromJson(item, defaultSource: 'kkphim');
    return m.copyWith(
      thumbUrl: m.thumbUrl.isNotEmpty && !m.thumbUrl.startsWith('http')
          ? 'https://phimimg.com/${m.thumbUrl}'
          : m.thumbUrl,
      posterUrl: m.posterUrl.isNotEmpty && !m.posterUrl.startsWith('http')
          ? 'https://phimimg.com/${m.posterUrl}'
          : m.posterUrl,
    );
  }

  static Movie _normalizeOphim(Map<String, dynamic> item) {
    var m = Movie.fromJson(item, defaultSource: 'ophim');
    return m.copyWith(
      thumbUrl: m.thumbUrl.isNotEmpty && !m.thumbUrl.startsWith('http')
          ? 'https://img.ophim.live/uploads/movies/${m.thumbUrl}'
          : m.thumbUrl,
      posterUrl: m.posterUrl.isNotEmpty && !m.posterUrl.startsWith('http')
          ? 'https://img.ophim.live/uploads/movies/${m.posterUrl}'
          : m.posterUrl,
    );
  }

  static Movie _normalizeVSMov(Map<String, dynamic> item) {
    String thumb = item['thumb_url'] ?? '';
    String poster = item['poster_url'] ?? '';
    if (thumb.isNotEmpty && !thumb.startsWith('http'))
      thumb = 'https://img.vsmcdn.com/$thumb';
    if (poster.isNotEmpty && !poster.startsWith('http'))
      poster = 'https://img.vsmcdn.com/$poster';

    var m = Movie.fromJson(item, defaultSource: 'vsmov');
    return m.copyWith(thumbUrl: thumb, posterUrl: poster);
  }

  static Movie _normalizePhim4K(Map<String, dynamic> item) {
    return Movie.fromJson(item, defaultSource: 'phim4k');
  }

  static Movie _normalizeFree1(Map<String, dynamic> item) {
    String thumb = item['thumb_url'] ?? '';
    String poster = item['poster_url'] ?? '';
    if (thumb.isNotEmpty && !thumb.startsWith('http'))
      thumb = 'https://img.phimapi.com/$thumb';
    if (poster.isNotEmpty && !poster.startsWith('http'))
      poster = 'https://img.phimapi.com/$poster';

    var m = Movie.fromJson(item, defaultSource: 'free1');
    return m.copyWith(thumbUrl: thumb, posterUrl: poster);
  }

  // --- Fetch Helper ---
  static Future<List<Movie>> _fetchSource(
    String url,
    Movie Function(Map<String, dynamic>) normalizer,
  ) async {
    try {
      final res = await http
          .get(Uri.parse(url))
          .timeout(const Duration(seconds: 5));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final items =
            (data['items'] as List?) ?? (data['data']?['items'] as List?) ?? [];
        return items.map((e) => normalizer(e as Map<String, dynamic>)).toList();
      }
    } catch (e) {
      // Ignore errors for individual sources to not break the merge
    }
    return [];
  }

  static Future<List<Movie>> _fetchPremiumSource(String url) async {
    try {
      final res = await http
          .get(Uri.parse(url))
          .timeout(const Duration(seconds: 15));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final items = (data['items'] as List?) ?? [];
        return items.map((e) {
          var map = Map<String, dynamic>.from(e as Map<String, dynamic>);
          final originalSlug = (map['slug'] ?? '')
              .toString(); // save original slug before overriding
          final type = map['type'] == 'series' ? 'series' : 'movie';
          final id = map['raw_payload'] ?? map['_id'];
          if (id != null) {
            map['slug'] = 'premium-$type-$id';
          }
          var m = Movie.fromJson(map, defaultSource: 'premium');
          // Store original slug so detail fetch can use it
          final newSlugs = Map<String, String>.from(m.sourceSlugs);
          newSlugs['premium_original'] = originalSlug;
          return m.copyWith(quality: 'Premium', sourceSlugs: newSlugs);
        }).toList();
      }
    } catch (e) {}
    return [];
  }

  // --- Merge Logic (Map by Slug) ---
  static List<Movie> _mergeMovieItems(
    List<Movie> itemsNguonC,
    List<Movie> itemsKKPhim,
    List<Movie> itemsOphim,
    List<Movie> itemsVSMov,
    List<Movie> itemsPhim4K,
    List<Movie> itemsFree1,
    List<Movie> itemsPremium,
    List<Movie> itemsMotchill,
    List<Movie> itemsStremio,
    List<Movie> itemsFilm4KNet,
  ) {
    final Map<String, Movie> mergedMap = {};

    bool isSimilarMovie(Movie a, Movie b) {
      String origA = a.originalName.isNotEmpty ? a.originalName : a.name;
      String origB = b.originalName.isNotEmpty ? b.originalName : b.name;

      if (origA.isNotEmpty && origB.isNotEmpty) {
        String normA = origA.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]'), '');
        String normB = origB.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]'), '');
        if (normA != normB &&
            !normA.contains(normB) &&
            !normB.contains(normA)) {
          return false;
        }
      }
      if (a.year.isNotEmpty && b.year.isNotEmpty && a.year != b.year) {
        return false;
      }
      return true;
    }

    Movie mergeItemInfo(Movie existing, Movie item) {
      bool isPremium = item.source == 'premium';
      Map<String, String> newSlugs = Map.from(existing.sourceSlugs);
      newSlugs.addAll(item.sourceSlugs);
      return existing.copyWith(
        thumbUrl: item.thumbUrl.isNotEmpty ? item.thumbUrl : existing.thumbUrl,
        posterUrl: item.posterUrl.isNotEmpty
            ? item.posterUrl
            : existing.posterUrl,
        currentEpisode:
            (item.currentEpisode.isNotEmpty &&
                item.currentEpisode != 'Đang cập nhật')
            ? item.currentEpisode
            : existing.currentEpisode,
        quality:
            (item.quality.isNotEmpty &&
                item.quality != 'FHD' &&
                item.quality != 'N/A')
            ? item.quality
            : existing.quality,
        time: (item.time.isNotEmpty && item.time != 'N/A')
            ? item.time
            : existing.time,
        language:
            (item.language.isNotEmpty &&
                item.language != 'Vietsub' &&
                item.language != 'N/A')
            ? item.language
            : existing.language,
        description:
            (item.source == 'stremio' && existing.description.isNotEmpty)
            ? existing.description
            : (isPremium && existing.description.isNotEmpty)
            ? existing.description
            : (item.description.isNotEmpty
                  ? item.description
                  : existing.description),
        year: item.year.isNotEmpty ? item.year : existing.year,
        genres: (isPremium && existing.genres.isNotEmpty)
            ? existing.genres
            : (item.genres.isNotEmpty ? item.genres : existing.genres),
        countries: item.countries.isNotEmpty
            ? item.countries
            : existing.countries,
        directors: item.directors.isNotEmpty
            ? item.directors
            : existing.directors,
        casts: (item.source == 'stremio' && existing.casts.isNotEmpty)
            ? existing.casts
            : (item.casts.isNotEmpty ? item.casts : existing.casts),
        sourceSlugs: newSlugs,
        source: existing.source != item.source ? 'mixed' : existing.source,
      );
    }

    void mergeList(List<Movie> items) {
      for (var item in items) {
        bool merged = false;
        String baseSlug = item.slug;

        // Tìm xem có phim nào trong danh sách đã gộp trùng tên không (bất kể slug là gì)
        for (var key in mergedMap.keys.toList()) {
          if (isSimilarMovie(mergedMap[key]!, item)) {
            mergedMap[key] = mergeItemInfo(mergedMap[key]!, item);
            merged = true;
            break;
          }
        }

        if (!merged) {
          for (int i = 0; i < 5; i++) {
            String keyToCheck = i == 0 ? baseSlug : '${baseSlug}_alt_$i';
            if (!mergedMap.containsKey(keyToCheck)) {
              mergedMap[keyToCheck] = item;
              break;
            }
          }
        }
      }
    }

    mergeList(itemsVSMov); // Thấp nhất
    mergeList(itemsKKPhim);
    mergeList(itemsOphim);
    mergeList(itemsNguonC);
    mergeList(itemsFree1);
    mergeList(itemsPhim4K);
    mergeList(itemsMotchill);
    mergeList(itemsFilm4KNet); // Nguồn chất lượng cao
    mergeList(itemsPremium); // Cao nhất
    mergeList(itemsStremio); // Rất cao để lấy poster

    int getPriority(Movie m) {
      if (m.sourceSlugs.containsKey('premium')) return 0;
      if (m.sourceSlugs.containsKey('film4knet')) return 1;
      if (m.sourceSlugs.containsKey('stremio')) return 2;
      if (m.sourceSlugs.containsKey('nguonc')) return 3;
      if (m.sourceSlugs.containsKey('ophim')) return 4;
      if (m.sourceSlugs.containsKey('kkphim')) return 5;
      if (m.sourceSlugs.containsKey('phim4k')) return 6;
      if (m.sourceSlugs.containsKey('free1')) return 7;
      if (m.sourceSlugs.containsKey('vsmov')) return 8;
      if (m.sourceSlugs.containsKey('motchill')) return 9;
      return 10;
    }

    final resultList = mergedMap.values.toList();
    resultList.sort((a, b) => getPriority(a).compareTo(getPriority(b)));

    return resultList;
  }

  // --- Fetch And Merge Wrapper ---
  static Future<List<Movie>> _fetchAndMerge(
    String urlNguonC,
    String urlKKPhim,
    String urlOphim,
    String urlVSMov,
    String urlPhim4K,
    String urlFree1,
    String premiumSuffix,
    Future<List<Movie>> Function() motchillFetcher,
    Future<List<Movie>> Function()? stremioFetcher,
    Future<List<Movie>> Function()? film4knetFetcher,
  ) async {
    final prefs = await SharedPreferences.getInstance();
    final enabledSources =
        prefs.getStringList('enabled_sources') ??
        [
          'premium',
          'nguonc',
          'ophim',
          'kkphim',
          'vsmov',
          'film4knet',
          'phim4k',
          'free1',
          'motchill',
        ];

    final futures = [
      enabledSources.contains('nguonc')
          ? _fetchSource(urlNguonC, _normalizeNguonC)
          : Future.value(<Movie>[]),
      enabledSources.contains('kkphim')
          ? _fetchSource(urlKKPhim, _normalizeKKPhim)
          : Future.value(<Movie>[]),
      enabledSources.contains('ophim')
          ? _fetchSource(urlOphim, _normalizeOphim)
          : Future.value(<Movie>[]),
      enabledSources.contains('vsmov')
          ? _fetchSource(urlVSMov, _normalizeVSMov)
          : Future.value(<Movie>[]),
      enabledSources.contains('phim4k')
          ? _fetchSource(urlPhim4K, _normalizePhim4K)
          : Future.value(<Movie>[]),
      enabledSources.contains('free1')
          ? _fetchSource(urlFree1, _normalizeFree1)
          : Future.value(<Movie>[]),
      enabledSources.contains('premium')
          ? _fetchPremiumSource(
              'https://dogtail.oxaliplatin.workers.dev/api/premium$premiumSuffix',
            )
          : Future.value(<Movie>[]),
      (enabledSources.contains('motchill'))
          ? motchillFetcher().catchError((_) => <Movie>[])
          : Future.value(<Movie>[]),
      (enabledSources.contains('torrentio') && stremioFetcher != null)
          ? stremioFetcher().catchError((_) => <Movie>[])
          : Future.value(<Movie>[]),
      (enabledSources.contains('film4knet') && film4knetFetcher != null)
          ? film4knetFetcher().catchError((_) => <Movie>[])
          : Future.value(<Movie>[]),
    ];

    final results = await Future.wait(futures);
    return _mergeMovieItems(
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
    );
  }

  // ================= ENDPOINTS =================

  static Future<List<Movie>> getNewUpdatedMovies({int page = 1}) async {
    return _fetchAndMerge(
      '$nguoncUrl/films/phim-moi-cap-nhat?page=$page',
      '$kkphimUrl/danh-sach/phim-moi-cap-nhat?page=$page',
      '$ophimUrl/danh-sach/phim-moi-cap-nhat?page=$page',
      '$vsmovUrl/danh-sach/phim-moi-cap-nhat?page=$page',
      '$phim4kUrl/films/phim-moi-cap-nhat?page=$page',
      '$free1List/phim-moi-cap-nhat-v3?page=$page',
      '/movies?page=$page',
      () => MotchillScraper.getRecent(page),
      null, // Don't fetch stremio for new updated because it takes too long/no pagination
      () => Film4kNetApi.getRecent(page),
    );
  }

  static Future<List<Movie>> getMoviesByCategory(
    String slug, {
    int page = 1,
  }) async {
    String vsmovType = slug;
    if (slug == 'phim-le')
      vsmovType = 'single';
    else if (slug == 'phim-bo')
      vsmovType = 'series';
    else if (slug == 'hoat-hinh')
      vsmovType = 'hoathinh';
    else if (slug == 'tv-shows')
      vsmovType = 'tvshows';

    return _fetchAndMerge(
      '$nguoncUrl/films/danh-sach/$slug?page=$page',
      '$kkphimUrl/danh-sach/$slug?page=$page',
      '$ophimUrl/danh-sach/$slug?page=$page',
      '$vsmovUrl/danh-sach?type=$vsmovType&page=$page',
      '$phim4kUrl/films/danh-sach/$slug?page=$page',
      '$free1Url/danh-sach/$slug?page=$page',
      '/movies?page=$page&filterType=danh-sach&filterValue=$slug',
      () => MotchillScraper.getByList(slug, page),
      null,
      null,
    );
  }

  static Future<List<Movie>> getMoviesByGenre(
    String slug, {
    int page = 1,
  }) async {
    return _fetchAndMerge(
      '$nguoncUrl/films/the-loai/$slug?page=$page',
      '$kkphimUrl/the-loai/$slug?page=$page',
      '$ophimUrl/the-loai/$slug?page=$page',
      '$vsmovUrl/the-loai/$slug?page=$page',
      '$phim4kUrl/films/the-loai/$slug?page=$page',
      '$free1Url/the-loai/$slug?page=$page',
      '/movies?page=$page&filterType=the-loai&filterValue=$slug',
      () => MotchillScraper.getByGenre(slug, page),
      null,
      null,
    );
  }

  static Future<List<Movie>> getMoviesByCountry(
    String slug, {
    int page = 1,
  }) async {
    return _fetchAndMerge(
      '$nguoncUrl/films/quoc-gia/$slug?page=$page',
      '$kkphimUrl/quoc-gia/$slug?page=$page',
      '$ophimUrl/quoc-gia/$slug?page=$page',
      '$vsmovUrl/quoc-gia/$slug?page=$page',
      '$phim4kUrl/films/quoc-gia/$slug?page=$page',
      '$free1Url/quoc-gia/$slug?page=$page',
      '/movies?page=$page&filterType=quoc-gia&filterValue=$slug',
      () => MotchillScraper.getByCountry(slug, page),
      null,
      null,
    );
  }

  static Future<List<Movie>> searchMovies(String keyword) async {
    final enc = Uri.encodeComponent(keyword);
    return _fetchAndMerge(
      '$nguoncUrl/films/search?keyword=$enc',
      '$kkphimUrl/tim-kiem?keyword=$enc',
      '$ophimUrl/tim-kiem?keyword=$enc',
      '$vsmovUrl/tim-kiem?keyword=$enc',
      '$phim4kUrl/films/search?keyword=$enc',
      '$free1Url/tim-kiem?keyword=$enc',
      '/movies?keyword=$enc',
      () => MotchillScraper.search(keyword),
      () => CinemetaApi.searchCinemeta(keyword),
      () => Film4kNetApi.search(keyword),
    );
  }

  // --- Detail Fetching ---
  static String _processM3u8Url(String url) {
    if (url.isEmpty) return url;
    if (url.contains('workers.dev') ||
        (url.contains('dpdns.org') && !url.contains('stream/hls'))) {
      final rawId = url.split('/').last;

      // TODO: Các server cũ đa phần bị 404 (Cloudflare xoá). Giữ lại ở đây để fix sau.
      /*
      final workers = [
        'demo.cryboiz.workers.dev',
        'sv1.gboiz.workers.dev',
        'sv1.gboiz2.workers.dev',
        'sv.phim4k.dpdns.org',
      ];
      for (int i = 3; i <= 35; i++) {
        workers.add('sv.gboiz$i.workers.dev');
      }
      workers.shuffle();
      return 'https://${workers.first}/$rawId';
      */

      final activeServers = ['sv.gboiz7.workers.dev', 'sv1.p4k.dpdns.org'];
      activeServers.shuffle();
      return 'https://${activeServers.first}/$rawId';
    }
    return url;
  }

  static List<EpisodeServer> _parseEpisodes(List rawEps, String prefix) {
    List<EpisodeServer> servers = [];
    for (var srv in rawEps) {
      String rawName = srv['server_name'] ?? 'Server';
      rawName = rawName.replaceAll(RegExp(r'#\d+|\s+\d+$'), '').trim();
      final serverName = prefix.isNotEmpty ? '$prefix - $rawName' : rawName;

      List epItems = [];
      if (srv['server_data'] is List) {
        epItems = srv['server_data'];
      } else if (srv['items'] is List) {
        epItems = srv['items'];
      }

      final episodes = epItems.map((ep) {
        String rawUrl = (ep['link_m3u8'] ?? ep['m3u8'] ?? ep['link'] ?? '')
            .toString();
        return Episode(
          name: (ep['name'] ?? '').toString(),
          slug: (ep['slug'] ?? '').toString(),
          m3u8Url: _processM3u8Url(rawUrl),
          embedUrl: (ep['link_embed'] ?? ep['embed'] ?? '').toString(),
        );
      }).toList();
      servers.add(EpisodeServer(serverName: serverName, items: episodes));
    }
    return servers;
  }

  static bool _isSimilarMovieGlobal(Movie? initial, Movie fetched) {
    if (initial == null) return true;
    if (initial.originalName.isNotEmpty && fetched.originalName.isNotEmpty) {
      String normA = initial.originalName.toLowerCase().replaceAll(
        RegExp(r'[^a-z0-9]'),
        '',
      );
      String normB = fetched.originalName.toLowerCase().replaceAll(
        RegExp(r'[^a-z0-9]'),
        '',
      );
      if (normA != normB && !normA.contains(normB) && !normB.contains(normA)) {
        return false;
      }
    }
    if (initial.year.isNotEmpty &&
        fetched.year.isNotEmpty &&
        initial.year != fetched.year) {
      return false;
    }
    return true;
  }


  static String _slugify(String text) {
    String lower = text.toLowerCase().trim();
    lower = lower.replaceAll(RegExp(r'[^a-z0-9\s]'), '');
    return lower.replaceAll(RegExp(r'\s+'), '-');
  }

  static Stream<Movie> fetchMovieDetailStream(

    String slug, {
    Movie? initialMovie,
  }) {
    final controller = StreamController<Movie>();
    final Map<int, Movie> parsedMap = {};
    final Map<int, List<EpisodeServer>> serversMap = {};

    void processAndEmit() {
      if (parsedMap.isEmpty) return;

      final order = [6, 3, 7, 1, 0, 2, 4, 5, 10, 8, 9];

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
        
        bool mergedHasBackdrop = merged.posterUrl.isNotEmpty && merged.posterUrl != merged.thumbUrl;
        bool itemHasBackdrop = item.posterUrl.isNotEmpty && item.posterUrl != item.thumbUrl;
        String bestPosterUrl = mergedHasBackdrop 
            ? merged.posterUrl 
            : (itemHasBackdrop ? item.posterUrl : (merged.posterUrl.isNotEmpty ? merged.posterUrl : item.posterUrl));

        merged = merged.copyWith(
          thumbUrl: merged.thumbUrl.isNotEmpty ? merged.thumbUrl : item.thumbUrl,
          posterUrl: bestPosterUrl,
          currentEpisode:
              (merged.currentEpisode.isNotEmpty &&
                  merged.currentEpisode != 'Đang cập nhật' &&
                  merged.currentEpisode != 'N/A')
              ? merged.currentEpisode
              : item.currentEpisode,
          quality:
              (merged.quality.isNotEmpty &&
                  merged.quality != 'N/A')
              ? merged.quality
              : item.quality,
          time: (merged.time.isNotEmpty && merged.time != 'N/A')
              ? merged.time
              : item.time,
          language:
              (merged.language.isNotEmpty &&
                  merged.language != 'N/A')
              ? merged.language
              : item.language,
          description: merged.description.isNotEmpty
              ? merged.description
              : item.description,
          year: merged.year.isNotEmpty ? merged.year : item.year,
          genres: merged.genres.isNotEmpty ? merged.genres : item.genres,
          countries: merged.countries.isNotEmpty ? merged.countries : item.countries,
          directors: merged.directors.isNotEmpty ? merged.directors : item.directors,
          casts: merged.casts.isNotEmpty ? merged.casts : item.casts,
          source: merged.source != item.source ? 'mixed' : merged.source,
        );
      }

      merged = merged.copyWith(
        episodes: allServers
            .where(
              (server) => server.items.any(
                (ep) => ep.m3u8Url.isNotEmpty || ep.embedUrl.isNotEmpty,
              ),
            )
            .toList(),
      );

      controller.add(merged);
    }

    SharedPreferences.getInstance().then((prefs) {
      final enabledSources =
          prefs.getStringList('enabled_sources') ??
          [
            'premium',
            'nguonc',
            'ophim',
            'kkphim',
            'vsmov',
            'film4knet',
            'phim4k',
            'free1',
            'motchill',
          ];
      final timeout = const Duration(seconds: 5);
      final List<Future> futures = [];

      if (enabledSources.contains('film4knet')) {
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
      }

      if (enabledSources.contains('nguonc')) {
        final querySlug = initialMovie?.sourceSlugs['nguonc'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$nguoncUrl/film/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = data['movie'] ?? data['item'];
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizeNguonC(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[0] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? dataItem['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[0] = _parseEpisodes(
                      epsList as List? ?? [],
                      'NguonC',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('kkphim')) {
        final querySlug = initialMovie?.sourceSlugs['kkphim'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$kkphimUrl/phim/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = (data['movie'] != null)
                      ? data['movie']
                      : (data['data'] != null ? data['data']['item'] : null);
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizeKKPhim(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[1] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? dataItem['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[1] = _parseEpisodes(
                      epsList as List? ?? [],
                      'KKPhim',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('ophim')) {
        final querySlug = initialMovie?.sourceSlugs['ophim'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$ophimUrl/phim/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = (data['data'] != null)
                      ? (data['data']['item'] ?? data['data']['movie'])
                      : (data['movie'] ?? data['item']);
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizeOphim(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[7] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? dataItem['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[7] = _parseEpisodes(
                      epsList as List? ?? [],
                      'Ophim',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('phim4k')) {
        final querySlug = initialMovie?.sourceSlugs['phim4k'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$phim4kUrl/film/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = data['movie'] ?? data['item'];
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizePhim4K(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[2] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? dataItem['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[2] = _parseEpisodes(
                      epsList as List? ?? [],
                      'Free2',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('vsmov')) {
        final querySlug = initialMovie?.sourceSlugs['vsmov'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$vsmovUrl/phim/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = data['movie'] ?? data['item'];
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizeVSMov(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[3] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? dataItem['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[3] = _parseEpisodes(
                      epsList as List? ?? [],
                      'VSMov',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('free1')) {
        final querySlug = initialMovie?.sourceSlugs['free1'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$free1Url/phim/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = (data['data'] != null)
                      ? data['data']['item']
                      : (data['movie'] ?? data['item']);
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizeFree1(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[4] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? data['data']['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[4] = _parseEpisodes(
                      epsList as List? ?? [],
                      'Free1',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('premium')) {
        Future<void> fetchPremium() async {
          // Helper: slug word overlap check (same as web version)
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

          print(
            '[Premium DEBUG] slug=$slug, querySlug=$querySlug, initialMovie sourceSlugs=${initialMovie?.sourceSlugs}',
          );

          // 1. Try with provided slug directly
          try {
            final res = await http
                .get(
                  Uri.parse(
                    'https://dogtail.oxaliplatin.workers.dev/api/premium/detail/$querySlug',
                  ),
                )
                .timeout(timeout);
            if (res.statusCode == 200) {
              final data = json.decode(res.body);
              if (data['movie'] != null || data['item'] != null) {
                movieData = data['movie'] ?? data['item'];

                // If episodes are empty and we used a premium-ID slug, try with the original slug
                final eps = movieData!['episodes'];
                final hasEmptyEps =
                    eps == null ||
                    (eps is List &&
                        (eps.isEmpty ||
                            eps.every((srv) {
                              final sd = srv['server_data'];
                              return sd == null || (sd is List && sd.isEmpty);
                            })));

                if (hasEmptyEps && querySlug.startsWith('premium-')) {
                  // Try the saved original slug from the list (stored when normalizing premium items)
                  String originalSlug =
                      initialMovie?.sourceSlugs['premium_original'] ?? '';
                  print(
                    '[Premium DEBUG] hasEmptyEps=true, originalSlug from sourceSlugs: "$originalSlug"',
                  );

                  // If not available, search by the movie name we got from the API response
                  if (originalSlug.isEmpty ||
                      originalSlug.startsWith('premium-')) {
                    final movieName =
                        (movieData!['name'] ?? movieData!['origin_name'] ?? '')
                            .toString();
                    final movieSlug = (movieData!['slug'] ?? '').toString();
                    // Use the slug from movieData if it's not a premium-ID format
                    if (movieSlug.isNotEmpty &&
                        !movieSlug.startsWith('premium-')) {
                      originalSlug = movieSlug;
                      print(
                        '[Premium DEBUG] Using slug from movieData response: "$originalSlug"',
                      );
                    } else if (movieName.isNotEmpty) {
                      // Search by name to find the right slug
                      final keyword = movieName.split(' ').take(5).join(' ');
                      print(
                        '[Premium DEBUG] Searching premium by name: "$keyword"',
                      );
                      try {
                        final searchRes = await http
                            .get(
                              Uri.parse(
                                'https://dogtail.oxaliplatin.workers.dev/api/premium/movies?keyword=${Uri.encodeComponent(keyword)}',
                              ),
                            )
                            .timeout(const Duration(seconds: 5));
                        if (searchRes.statusCode == 200) {
                          final searchData = json.decode(searchRes.body);
                          final items = (searchData['items'] as List?) ?? [];
                          for (var item in items) {
                            if (item is Map<String, dynamic>) {
                              final itemSlug = (item['slug'] ?? '').toString();
                              if (itemSlug.isNotEmpty &&
                                  !itemSlug.startsWith('premium-')) {
                                originalSlug = itemSlug;
                                print(
                                  '[Premium DEBUG] Found original slug via search: "$originalSlug"',
                                );
                                break;
                              }
                            }
                          }
                        }
                      } catch (e) {}
                    }
                  }

                  if (originalSlug.isNotEmpty &&
                      originalSlug != querySlug &&
                      !originalSlug.startsWith('premium-')) {
                    print(
                      '[Premium DEBUG] Refetching with original slug: $originalSlug',
                    );
                    try {
                      final res2 = await http
                          .get(
                            Uri.parse(
                              'https://dogtail.oxaliplatin.workers.dev/api/premium/detail/$originalSlug',
                            ),
                          )
                          .timeout(timeout);
                      if (res2.statusCode == 200) {
                        final data2 = json.decode(res2.body);
                        final d2 = data2['movie'] ?? data2['item'];
                        if (d2 != null) {
                          final eps2 = d2['episodes'];
                          final hasEps2 =
                              eps2 is List &&
                              eps2.isNotEmpty &&
                              eps2.any((srv) {
                                final sd = srv['server_data'];
                                return sd is List && sd.isNotEmpty;
                              });
                          if (hasEps2) {
                            print(
                              '[Premium DEBUG] Refetch successful with $originalSlug, episodes found!',
                            );
                            movieData = d2;
                          }
                        }
                      }
                    } catch (e) {}
                  }
                }
              }
            }
          } catch (e) {}

          // 2. If not found, try slug variations (like the web version)
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
                  final res = await http
                      .get(
                        Uri.parse(
                          'https://dogtail.oxaliplatin.workers.dev/api/premium/detail/$v',
                        ),
                      )
                      .timeout(const Duration(seconds: 5));
                  if (res.statusCode == 200) {
                    final data = json.decode(res.body);
                    if (data['movie'] != null || data['item'] != null) {
                      movieData = data['movie'] ?? data['item'];
                      break;
                    }
                  }
                } catch (e) {}
              }
            }
          }

          // 3. If still not found, search by keyword with slug word overlap (like web version)
          if (movieData == null && !querySlug.startsWith('premium-')) {
            final words = slug.split('-');
            final keywords = [
              slug.replaceAll('-', ' '),
              words.isNotEmpty ? words[0] : '',
              words.length > 1 ? words.skip(1).join(' ') : '',
            ].where((kw) => kw.length > 2).toSet().toList();

            for (var kw in keywords) {
              try {
                final searchUrl =
                    'https://dogtail.oxaliplatin.workers.dev/api/premium/movies?keyword=${Uri.encodeComponent(kw)}';
                final res = await http
                    .get(Uri.parse(searchUrl))
                    .timeout(const Duration(seconds: 6));
                if (res.statusCode == 200) {
                  final searchData = json.decode(res.body);
                  final items = (searchData['items'] as List?) ?? [];
                  Map<String, dynamic>? bestMatch;

                  for (var item in items) {
                    if (item is! Map<String, dynamic>) continue;
                    final itemSlug = (item['slug'] ?? '').toString();
                    // Use slug word overlap (same as web version)
                    if (slugMatches(itemSlug)) {
                      bestMatch = item;
                      break;
                    }
                    // Also check if initialMovie name matches
                    if (initialMovie != null &&
                        _isSimilarMovieGlobal(
                          initialMovie,
                          Movie.fromJson(item, defaultSource: 'premium'),
                        )) {
                      bestMatch = item;
                      break;
                    }
                  }

                  if (bestMatch != null) {
                    final bestSlug = (bestMatch['slug'] ?? '').toString();
                    // If slug matches, use it directly
                    Map<String, dynamic>? detailData;
                    if (bestSlug != slug) {
                      try {
                        final detailRes = await http
                            .get(
                              Uri.parse(
                                'https://dogtail.oxaliplatin.workers.dev/api/premium/detail/$bestSlug',
                              ),
                            )
                            .timeout(const Duration(seconds: 6));
                        if (detailRes.statusCode == 200) {
                          final dd = json.decode(detailRes.body);
                          if (dd['movie'] != null || dd['item'] != null) {
                            detailData = dd;
                          }
                        }
                      } catch (e) {}
                    }
                    // Also try with premium-type-id format
                    if (detailData == null) {
                      final type = bestMatch['type'] == 'series'
                          ? 'series'
                          : 'movie';
                      final id = bestMatch['raw_payload'] ?? bestMatch['_id'];
                      if (id != null) {
                        try {
                          final matchedUrl =
                              'https://dogtail.oxaliplatin.workers.dev/api/premium/detail/premium-$type-$id';
                          final detailRes = await http
                              .get(Uri.parse(matchedUrl))
                              .timeout(const Duration(seconds: 6));
                          if (detailRes.statusCode == 200) {
                            final dd = json.decode(detailRes.body);
                            if (dd['movie'] != null || dd['item'] != null) {
                              detailData = dd;
                            }
                          }
                        } catch (e) {}
                      }
                    }
                    if (detailData != null) {
                      movieData = detailData['movie'] ?? detailData['item'];
                      break;
                    }
                  }
                }
              } catch (e) {}
              if (movieData != null) break;
            }
          }

          if (movieData != null) {
            var m = Movie.fromJson(
              movieData as Map<String, dynamic>,
              defaultSource: 'premium',
            ).copyWith(quality: 'Premium');
            // Don't reject if _isSimilarMovieGlobal returns false due to missing data — we already matched by slug overlap
            parsedMap[5] = m;

            List<EpisodeServer> premiumServers = [];
            final rawEpisodes = movieData['episodes'];
            print(
              '[Premium DEBUG] movieData keys: ${(movieData as Map).keys.toList()}',
            );
            print(
              '[Premium DEBUG] rawEpisodes type: ${rawEpisodes?.runtimeType}, value: $rawEpisodes',
            );
            final premEps = (rawEpisodes is List) ? rawEpisodes : [];
            print('[Premium DEBUG] premEps count: ${premEps.length}');
            for (var srv in premEps) {
              print(
                '[Premium DEBUG] srv type: ${srv.runtimeType}, keys: ${(srv as Map).keys.toList()}',
              );
              final serverName = (srv['server_name'] ?? 'Premium Server')
                  .toString();
              final serverData = srv['server_data'];
              final serverItems = srv['items'];
              print(
                '[Premium DEBUG] server_data type: ${serverData?.runtimeType}, items type: ${serverItems?.runtimeType}',
              );
              List epItems = (serverData is List)
                  ? serverData
                  : ((serverItems is List) ? serverItems : []);
              print('[Premium DEBUG] epItems count: ${epItems.length}');
              final episodes = epItems.map((ep) {
                final link = (ep['link'] ?? ep['link_m3u8'] ?? '').toString();
                final processed = _processM3u8Url(link);
                print(
                  '[Premium DEBUG] ep name: ${ep['name']}, link: $link, processed: $processed',
                );
                return Episode(
                  name: (ep['name'] ?? '').toString(),
                  slug: (ep['slug'] ?? '').toString(),
                  m3u8Url: processed,
                  embedUrl: (ep['link_embed'] ?? ep['embed'] ?? '').toString(),
                );
              }).toList();
              premiumServers.add(
                EpisodeServer(serverName: serverName, items: episodes),
              );
            }
            print(
              '[Premium DEBUG] premiumServers count: ${premiumServers.length}',
            );
            serversMap[5] = premiumServers;
            processAndEmit();
          }
        }

        futures.add(fetchPremium());
      }

      if (enabledSources.contains('motchill')) {
        final querySlug = initialMovie?.sourceSlugs['motchill'] ?? slug;
        futures.add(
          MotchillScraper.getDetail(querySlug)
              .timeout(timeout)
              .then((motchillData) {
                if (motchillData != null) {
                  if (!_isSimilarMovieGlobal(initialMovie, motchillData))
                    return;

                  parsedMap[6] = motchillData;
                  serversMap[6] = motchillData.episodes;
                  processAndEmit();
                }
              })
              .catchError((_) {}),
        );
      } // Added missing brace

      if (initialMovie != null &&
          (initialMovie.imdbId == null ||
              initialMovie.imdbId!.isEmpty ||
              initialMovie.imdbId == 'N/A')) {
        futures.add(() async {
          try {
            final isTv =
                initialMovie.type.toLowerCase() == 'series' ||
                initialMovie.type.toLowerCase() == 'tvshows' ||
                initialMovie.currentEpisode.toLowerCase().contains('tập') ||
                initialMovie.currentEpisode.contains('/') ||
                initialMovie.time.toLowerCase().contains('tập') ||
                initialMovie.episodes.any((e) => e.items.length > 1);

            final id = await TorrentioApi.getImdbId(
              initialMovie.name,
              initialMovie.originalName,
              initialMovie.year,
              isTv,
            );
            if (id != null && id.isNotEmpty) {
              if (parsedMap.isNotEmpty) {
                for (var key in parsedMap.keys) {
                  parsedMap[key] = parsedMap[key]!.copyWith(imdbId: id);
                }
                processAndEmit();
              }
            }
          } catch (_) {}
        }());
      }

      if ((enabledSources.contains('torrentio') ||
              enabledSources.contains('vidsrc') ||
              enabledSources.contains('vidapi')) &&
          initialMovie != null) {
        futures.add(() async {
          try {
            String imdbId =
                initialMovie.sourceSlugs['torrentio'] ??
                initialMovie.sourceSlugs['stremio'] ??
                '';
            final isTv =
                initialMovie.type.toLowerCase() == 'series' ||
                initialMovie.type.toLowerCase() == 'tvshows' ||
                initialMovie.currentEpisode.toLowerCase().contains('tập') ||
                initialMovie.currentEpisode.contains('/') ||
                initialMovie.time.toLowerCase().contains('tập') ||
                initialMovie.episodes.any((e) => e.items.length > 1);

            if (initialMovie.source == 'stremio' && imdbId.isNotEmpty) {
              // Fetch full metadata from Cinemeta
              final meta = await CinemetaApi.getMetaDetail(
                imdbId,
                isSeries: isTv,
              );
              if (meta != null) {
                parsedMap[8] = meta; // Use index 8 for stremio meta
                processAndEmit();
              }
            }

            if (imdbId.isEmpty &&
                initialMovie.imdbId != null &&
                initialMovie.imdbId!.isNotEmpty) {
              imdbId = initialMovie.imdbId!;
            }

            if (imdbId.isEmpty) {
              final id = await TorrentioApi.getImdbId(
                initialMovie.name,
                initialMovie.originalName,
                initialMovie.year,
                isTv,
              );
              if (id != null) imdbId = id;
            }

            if (imdbId.isNotEmpty) {
              // Update the initial movie with the found IMDB ID so UI can use it
              if (parsedMap.isNotEmpty) {
                final firstKey = parsedMap.keys.first;
                parsedMap[firstKey] = parsedMap[firstKey]!.copyWith(
                  imdbId: imdbId,
                );
              }

              final tmdbId = await TorrentioApi.getTmdbIdFromImdb(imdbId);

              // Check if it's a TV show, if so we don't fetch streams here, we just emit the imdbId
              // and fetch the episodes list from Cinemeta
              if (isTv) {
                final cinemetaEpisodes = await CinemetaApi.getSeriesEpisodes(
                  imdbId,
                );
                if (cinemetaEpisodes.isNotEmpty) {
                  final p2pItems = cinemetaEpisodes
                      .map(
                        (e) => Episode(
                          name: 'Tập ${e['episode']}',
                          slug: 'S${e['season']}E${e['episode']}',
                          m3u8Url:
                              'torrentio://$imdbId:${e['season']}:${e['episode']}',
                          embedUrl: '',
                        ),
                      )
                      .toList();

                  final vidsrcItems = tmdbId != null
                      ? cinemetaEpisodes
                            .map(
                              (e) => Episode(
                                name: 'Tập ${e['episode']}',
                                slug: 'S${e['season']}E${e['episode']}',
                                m3u8Url: '',
                                embedUrl:
                                    'https://vidsrc.sbs/embed/tv/$tmdbId/${e['season']}/${e['episode']}',
                              ),
                            )
                            .toList()
                      : <Episode>[];

                  final vidApiItems = cinemetaEpisodes
                      .map(
                        (e) => Episode(
                          name: 'Tập ${e['episode']}',
                          slug: 'S${e['season']}E${e['episode']}',
                          m3u8Url: '',
                          embedUrl:
                              'https://vaplayer.ru/embed/tv/$imdbId/${e['season']}/${e['episode']}',
                        ),
                      )
                      .toList();

                  serversMap[9] = [
                    EpisodeServer(serverName: 'P2P (Torrent)', items: p2pItems),
                    if (vidsrcItems.isNotEmpty)
                      EpisodeServer(
                        serverName: 'VidSrc (Embed)',
                        items: vidsrcItems,
                      ),
                    EpisodeServer(
                      serverName: 'VidAPI (Embed)',
                      items: vidApiItems,
                    ),
                  ];
                }
                processAndEmit();
                return;
              }

              final servers = enabledSources.contains('torrentio')
                  ? await TorrentioApi.fetchStreams(imdbId)
                  : <EpisodeServer>[];

              final vidsrcServer =
                  (tmdbId != null && enabledSources.contains('vidsrc'))
                  ? EpisodeServer(
                      serverName: 'VidSrc (Embed)',
                      items: [
                        Episode(
                          name: 'Full',
                          slug: 'full',
                          m3u8Url: '',
                          embedUrl: 'https://vidsrc.sbs/embed/movie/$tmdbId',
                        ),
                      ],
                    )
                  : null;

              final vidApiServer = enabledSources.contains('vidapi')
                  ? EpisodeServer(
                      serverName: 'VidAPI (Embed)',
                      items: [
                        Episode(
                          name: 'Full',
                          slug: 'full',
                          m3u8Url: '',
                          embedUrl: 'https://vaplayer.ru/embed/movie/$imdbId',
                        ),
                      ],
                    )
                  : null;

              if (servers.isNotEmpty) {
                if (vidsrcServer != null) servers.add(vidsrcServer);
                if (vidApiServer != null)
                  servers.add(vidApiServer as EpisodeServer);
                serversMap[9] = servers;
                processAndEmit();
              } else {
                serversMap[9] = [
                  if (vidsrcServer != null) vidsrcServer,
                  if (vidApiServer != null) vidApiServer,
                ];
                processAndEmit();
              }
            }
          } catch (e) {
            print('PhimApi torrentio error: $e');
          }
        }());
      }

      Future.wait(futures)
          .then((_) {
            processAndEmit();
            controller.close();
          })
          .catchError((_) {
            controller.close();
          });
    });

    return controller.stream;
  }

  static const String _tmdbApiKey = 'e9e9d8da18ae29fc430845952232787c';

  static Future<Map<String, dynamic>?> _searchTmdb(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    String type = isTvSeries ? 'tv' : 'movie';
    final query = Uri.encodeComponent(
      originalTitle.isNotEmpty ? originalTitle : title,
    );
    final searchUrl =
        'https://api.themoviedb.org/3/search/multi?query=$query&api_key=$_tmdbApiKey&language=vi-VN';

    try {
      final res = await http.get(Uri.parse(searchUrl));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        if (data['results'] != null && data['results'].isNotEmpty) {
          var match = data['results'][0];
          if (year.isNotEmpty) {
            final yMatch = data['results'].firstWhere(
              (r) => (r['release_date'] ?? r['first_air_date'] ?? '')
                  .toString()
                  .startsWith(year),
              orElse: () => null,
            );
            if (yMatch != null) match = yMatch;
          }
          return {
            'id': match['id']?.toString(),
            'type': match['media_type'] ?? type,
            'tmdbRating': match['vote_average']?.toString(),
            'backdrop_path': match['backdrop_path'],
          };
        }
      }
    } catch (e) {
      print('PhimApi _searchTmdb error: $e');
    }
    return null;
  }

  static Future<List<String>> getMovieImages(Movie movie) async {
    try {
      String? tmdbId;
      String type = (movie.type == 'series' || movie.type == 'hoathinh')
          ? 'tv'
          : 'movie';

      // 1. Cố gắng tìm bằng IMDB ID trước nếu có (chính xác nhất)
      if (movie.imdbId != null &&
          movie.imdbId!.isNotEmpty &&
          movie.imdbId != 'N/A') {
        final findUrl =
            'https://api.themoviedb.org/3/find/${movie.imdbId}?external_source=imdb_id&api_key=$_tmdbApiKey';
        final findRes = await http
            .get(Uri.parse(findUrl))
            .timeout(const Duration(seconds: 10));
        if (findRes.statusCode == 200) {
          final findData = json.decode(findRes.body);
          if (findData['movie_results'] != null &&
              findData['movie_results'].isNotEmpty) {
            tmdbId = findData['movie_results'][0]['id'].toString();
            type = 'movie';
          } else if (findData['tv_results'] != null &&
              findData['tv_results'].isNotEmpty) {
            tmdbId = findData['tv_results'][0]['id'].toString();
            type = 'tv';
          }
        }
      }

      // 2. Nếu không có hoặc không tìm thấy, dùng searchTmdb
      if (tmdbId == null) {
        final match = await _searchTmdb(
          movie.name,
          movie.originalName,
          movie.year,
          movie.type == 'series' || movie.type == 'hoathinh',
        );
        if (match != null && match['id'] != null) {
          tmdbId = match['id'].toString();
          type = match['type'] ?? type;
        }
      }

      // 3. Lấy ảnh từ TMDB
      if (tmdbId != null) {
        final imgUrl =
            'https://api.themoviedb.org/3/$type/$tmdbId/images?api_key=$_tmdbApiKey';
        final imgRes = await http
            .get(Uri.parse(imgUrl))
            .timeout(const Duration(seconds: 10));
        if (imgRes.statusCode == 200) {
          final imgData = json.decode(imgRes.body);
          List<String> imageUrls = [];

          if (imgData['backdrops'] != null) {
            final backdrops = imgData['backdrops'] as List;
            imageUrls.addAll(
              backdrops
                  .take(20)
                  .map(
                    (e) =>
                        'https://image.tmdb.org/t/p/original${e['file_path']}',
                  ),
            );
          }
          if (imgData['posters'] != null) {
            final posters = imgData['posters'] as List;
            imageUrls.addAll(
              posters
                  .take(10)
                  .map(
                    (e) =>
                        'https://image.tmdb.org/t/p/original${e['file_path']}',
                  ),
            );
          }

          return imageUrls;
        }
      }
    } catch (e) {
      print('PhimApi getMovieImages error: $e');
    }
    return [];
  }

    static Future<String?> getMovieTmdbLogo(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
    String language,
  ) async {
    try {
      final match = await _searchTmdb(title, originalTitle, year, isTvSeries);
      if (match != null && match['id'] != null) {
        final imgUrl =
            'https://api.themoviedb.org/3/${match['type']}/${match['id']}/images?api_key=import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:youtube_explode_dart/youtube_explode_dart.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/movie.dart';
import 'motchill_scraper.dart';
import 'film4knet_api.dart';
import 'torrentio_api.dart';
import 'cinemeta_api.dart';

class PhimApi {
  static const String nguoncUrl = 'https://phim.nguonc.com/api';
  static const String kkphimUrl = 'https://phimapi.com/v1/api';
  static const String ophimUrl = 'https://ophim1.com/v1/api';
  static const String vsmovUrl = 'https://vsmov.com/api';
  static const String phim4kUrl = 'https://free2.phim4k.lol/api';
  static const String free1Url = 'https://free1.phim4k.lol/v1/api';
  static const String premiumUrl =
      'https://dogtail.oxaliplatin.workers.dev/api/premium';
  static const String free1List = 'https://free1.phim4k.lol/danh-sach';

  // --- Normalization functions ---
  static Movie _normalizeNguonC(Map<String, dynamic> item) {
    return Movie.fromJson(item, defaultSource: 'nguonc');
  }

  static Movie _normalizeKKPhim(Map<String, dynamic> item) {
    var m = Movie.fromJson(item, defaultSource: 'kkphim');
    return m.copyWith(
      thumbUrl: m.thumbUrl.isNotEmpty && !m.thumbUrl.startsWith('http')
          ? 'https://phimimg.com/${m.thumbUrl}'
          : m.thumbUrl,
      posterUrl: m.posterUrl.isNotEmpty && !m.posterUrl.startsWith('http')
          ? 'https://phimimg.com/${m.posterUrl}'
          : m.posterUrl,
    );
  }

  static Movie _normalizeOphim(Map<String, dynamic> item) {
    var m = Movie.fromJson(item, defaultSource: 'ophim');
    return m.copyWith(
      thumbUrl: m.thumbUrl.isNotEmpty && !m.thumbUrl.startsWith('http')
          ? 'https://img.ophim.live/uploads/movies/${m.thumbUrl}'
          : m.thumbUrl,
      posterUrl: m.posterUrl.isNotEmpty && !m.posterUrl.startsWith('http')
          ? 'https://img.ophim.live/uploads/movies/${m.posterUrl}'
          : m.posterUrl,
    );
  }

  static Movie _normalizeVSMov(Map<String, dynamic> item) {
    String thumb = item['thumb_url'] ?? '';
    String poster = item['poster_url'] ?? '';
    if (thumb.isNotEmpty && !thumb.startsWith('http'))
      thumb = 'https://img.vsmcdn.com/$thumb';
    if (poster.isNotEmpty && !poster.startsWith('http'))
      poster = 'https://img.vsmcdn.com/$poster';

    var m = Movie.fromJson(item, defaultSource: 'vsmov');
    return m.copyWith(thumbUrl: thumb, posterUrl: poster);
  }

  static Movie _normalizePhim4K(Map<String, dynamic> item) {
    return Movie.fromJson(item, defaultSource: 'phim4k');
  }

  static Movie _normalizeFree1(Map<String, dynamic> item) {
    String thumb = item['thumb_url'] ?? '';
    String poster = item['poster_url'] ?? '';
    if (thumb.isNotEmpty && !thumb.startsWith('http'))
      thumb = 'https://img.phimapi.com/$thumb';
    if (poster.isNotEmpty && !poster.startsWith('http'))
      poster = 'https://img.phimapi.com/$poster';

    var m = Movie.fromJson(item, defaultSource: 'free1');
    return m.copyWith(thumbUrl: thumb, posterUrl: poster);
  }

  // --- Fetch Helper ---
  static Future<List<Movie>> _fetchSource(
    String url,
    Movie Function(Map<String, dynamic>) normalizer,
  ) async {
    try {
      final res = await http
          .get(Uri.parse(url))
          .timeout(const Duration(seconds: 5));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final items =
            (data['items'] as List?) ?? (data['data']?['items'] as List?) ?? [];
        return items.map((e) => normalizer(e as Map<String, dynamic>)).toList();
      }
    } catch (e) {
      // Ignore errors for individual sources to not break the merge
    }
    return [];
  }

  static Future<List<Movie>> _fetchPremiumSource(String url) async {
    try {
      final res = await http
          .get(Uri.parse(url))
          .timeout(const Duration(seconds: 15));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final items = (data['items'] as List?) ?? [];
        return items.map((e) {
          var map = Map<String, dynamic>.from(e as Map<String, dynamic>);
          final originalSlug = (map['slug'] ?? '')
              .toString(); // save original slug before overriding
          final type = map['type'] == 'series' ? 'series' : 'movie';
          final id = map['raw_payload'] ?? map['_id'];
          if (id != null) {
            map['slug'] = 'premium-$type-$id';
          }
          var m = Movie.fromJson(map, defaultSource: 'premium');
          // Store original slug so detail fetch can use it
          final newSlugs = Map<String, String>.from(m.sourceSlugs);
          newSlugs['premium_original'] = originalSlug;
          return m.copyWith(quality: 'Premium', sourceSlugs: newSlugs);
        }).toList();
      }
    } catch (e) {}
    return [];
  }

  // --- Merge Logic (Map by Slug) ---
  static List<Movie> _mergeMovieItems(
    List<Movie> itemsNguonC,
    List<Movie> itemsKKPhim,
    List<Movie> itemsOphim,
    List<Movie> itemsVSMov,
    List<Movie> itemsPhim4K,
    List<Movie> itemsFree1,
    List<Movie> itemsPremium,
    List<Movie> itemsMotchill,
    List<Movie> itemsStremio,
    List<Movie> itemsFilm4KNet,
  ) {
    final Map<String, Movie> mergedMap = {};

    bool isSimilarMovie(Movie a, Movie b) {
      String origA = a.originalName.isNotEmpty ? a.originalName : a.name;
      String origB = b.originalName.isNotEmpty ? b.originalName : b.name;

      if (origA.isNotEmpty && origB.isNotEmpty) {
        String normA = origA.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]'), '');
        String normB = origB.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]'), '');
        if (normA != normB &&
            !normA.contains(normB) &&
            !normB.contains(normA)) {
          return false;
        }
      }
      if (a.year.isNotEmpty && b.year.isNotEmpty && a.year != b.year) {
        return false;
      }
      return true;
    }

    Movie mergeItemInfo(Movie existing, Movie item) {
      bool isPremium = item.source == 'premium';
      Map<String, String> newSlugs = Map.from(existing.sourceSlugs);
      newSlugs.addAll(item.sourceSlugs);
      return existing.copyWith(
        thumbUrl: item.thumbUrl.isNotEmpty ? item.thumbUrl : existing.thumbUrl,
        posterUrl: item.posterUrl.isNotEmpty
            ? item.posterUrl
            : existing.posterUrl,
        currentEpisode:
            (item.currentEpisode.isNotEmpty &&
                item.currentEpisode != 'Đang cập nhật')
            ? item.currentEpisode
            : existing.currentEpisode,
        quality:
            (item.quality.isNotEmpty &&
                item.quality != 'FHD' &&
                item.quality != 'N/A')
            ? item.quality
            : existing.quality,
        time: (item.time.isNotEmpty && item.time != 'N/A')
            ? item.time
            : existing.time,
        language:
            (item.language.isNotEmpty &&
                item.language != 'Vietsub' &&
                item.language != 'N/A')
            ? item.language
            : existing.language,
        description:
            (item.source == 'stremio' && existing.description.isNotEmpty)
            ? existing.description
            : (isPremium && existing.description.isNotEmpty)
            ? existing.description
            : (item.description.isNotEmpty
                  ? item.description
                  : existing.description),
        year: item.year.isNotEmpty ? item.year : existing.year,
        genres: (isPremium && existing.genres.isNotEmpty)
            ? existing.genres
            : (item.genres.isNotEmpty ? item.genres : existing.genres),
        countries: item.countries.isNotEmpty
            ? item.countries
            : existing.countries,
        directors: item.directors.isNotEmpty
            ? item.directors
            : existing.directors,
        casts: (item.source == 'stremio' && existing.casts.isNotEmpty)
            ? existing.casts
            : (item.casts.isNotEmpty ? item.casts : existing.casts),
        sourceSlugs: newSlugs,
        source: existing.source != item.source ? 'mixed' : existing.source,
      );
    }

    void mergeList(List<Movie> items) {
      for (var item in items) {
        bool merged = false;
        String baseSlug = item.slug;

        // Tìm xem có phim nào trong danh sách đã gộp trùng tên không (bất kể slug là gì)
        for (var key in mergedMap.keys.toList()) {
          if (isSimilarMovie(mergedMap[key]!, item)) {
            mergedMap[key] = mergeItemInfo(mergedMap[key]!, item);
            merged = true;
            break;
          }
        }

        if (!merged) {
          for (int i = 0; i < 5; i++) {
            String keyToCheck = i == 0 ? baseSlug : '${baseSlug}_alt_$i';
            if (!mergedMap.containsKey(keyToCheck)) {
              mergedMap[keyToCheck] = item;
              break;
            }
          }
        }
      }
    }

    mergeList(itemsVSMov); // Thấp nhất
    mergeList(itemsKKPhim);
    mergeList(itemsOphim);
    mergeList(itemsNguonC);
    mergeList(itemsFree1);
    mergeList(itemsPhim4K);
    mergeList(itemsMotchill);
    mergeList(itemsFilm4KNet); // Nguồn chất lượng cao
    mergeList(itemsPremium); // Cao nhất
    mergeList(itemsStremio); // Rất cao để lấy poster

    int getPriority(Movie m) {
      if (m.sourceSlugs.containsKey('premium')) return 0;
      if (m.sourceSlugs.containsKey('film4knet')) return 1;
      if (m.sourceSlugs.containsKey('stremio')) return 2;
      if (m.sourceSlugs.containsKey('nguonc')) return 3;
      if (m.sourceSlugs.containsKey('ophim')) return 4;
      if (m.sourceSlugs.containsKey('kkphim')) return 5;
      if (m.sourceSlugs.containsKey('phim4k')) return 6;
      if (m.sourceSlugs.containsKey('free1')) return 7;
      if (m.sourceSlugs.containsKey('vsmov')) return 8;
      if (m.sourceSlugs.containsKey('motchill')) return 9;
      return 10;
    }

    final resultList = mergedMap.values.toList();
    resultList.sort((a, b) => getPriority(a).compareTo(getPriority(b)));

    return resultList;
  }

  // --- Fetch And Merge Wrapper ---
  static Future<List<Movie>> _fetchAndMerge(
    String urlNguonC,
    String urlKKPhim,
    String urlOphim,
    String urlVSMov,
    String urlPhim4K,
    String urlFree1,
    String premiumSuffix,
    Future<List<Movie>> Function() motchillFetcher,
    Future<List<Movie>> Function()? stremioFetcher,
    Future<List<Movie>> Function()? film4knetFetcher,
  ) async {
    final prefs = await SharedPreferences.getInstance();
    final enabledSources =
        prefs.getStringList('enabled_sources') ??
        [
          'premium',
          'nguonc',
          'ophim',
          'kkphim',
          'vsmov',
          'film4knet',
          'phim4k',
          'free1',
          'motchill',
        ];

    final futures = [
      enabledSources.contains('nguonc')
          ? _fetchSource(urlNguonC, _normalizeNguonC)
          : Future.value(<Movie>[]),
      enabledSources.contains('kkphim')
          ? _fetchSource(urlKKPhim, _normalizeKKPhim)
          : Future.value(<Movie>[]),
      enabledSources.contains('ophim')
          ? _fetchSource(urlOphim, _normalizeOphim)
          : Future.value(<Movie>[]),
      enabledSources.contains('vsmov')
          ? _fetchSource(urlVSMov, _normalizeVSMov)
          : Future.value(<Movie>[]),
      enabledSources.contains('phim4k')
          ? _fetchSource(urlPhim4K, _normalizePhim4K)
          : Future.value(<Movie>[]),
      enabledSources.contains('free1')
          ? _fetchSource(urlFree1, _normalizeFree1)
          : Future.value(<Movie>[]),
      enabledSources.contains('premium')
          ? _fetchPremiumSource(
              'https://dogtail.oxaliplatin.workers.dev/api/premium$premiumSuffix',
            )
          : Future.value(<Movie>[]),
      (enabledSources.contains('motchill'))
          ? motchillFetcher().catchError((_) => <Movie>[])
          : Future.value(<Movie>[]),
      (enabledSources.contains('torrentio') && stremioFetcher != null)
          ? stremioFetcher().catchError((_) => <Movie>[])
          : Future.value(<Movie>[]),
      (enabledSources.contains('film4knet') && film4knetFetcher != null)
          ? film4knetFetcher().catchError((_) => <Movie>[])
          : Future.value(<Movie>[]),
    ];

    final results = await Future.wait(futures);
    return _mergeMovieItems(
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
    );
  }

  // ================= ENDPOINTS =================

  static Future<List<Movie>> getNewUpdatedMovies({int page = 1}) async {
    return _fetchAndMerge(
      '$nguoncUrl/films/phim-moi-cap-nhat?page=$page',
      '$kkphimUrl/danh-sach/phim-moi-cap-nhat?page=$page',
      '$ophimUrl/danh-sach/phim-moi-cap-nhat?page=$page',
      '$vsmovUrl/danh-sach/phim-moi-cap-nhat?page=$page',
      '$phim4kUrl/films/phim-moi-cap-nhat?page=$page',
      '$free1List/phim-moi-cap-nhat-v3?page=$page',
      '/movies?page=$page',
      () => MotchillScraper.getRecent(page),
      null, // Don't fetch stremio for new updated because it takes too long/no pagination
      () => Film4kNetApi.getRecent(page),
    );
  }

  static Future<List<Movie>> getMoviesByCategory(
    String slug, {
    int page = 1,
  }) async {
    String vsmovType = slug;
    if (slug == 'phim-le')
      vsmovType = 'single';
    else if (slug == 'phim-bo')
      vsmovType = 'series';
    else if (slug == 'hoat-hinh')
      vsmovType = 'hoathinh';
    else if (slug == 'tv-shows')
      vsmovType = 'tvshows';

    return _fetchAndMerge(
      '$nguoncUrl/films/danh-sach/$slug?page=$page',
      '$kkphimUrl/danh-sach/$slug?page=$page',
      '$ophimUrl/danh-sach/$slug?page=$page',
      '$vsmovUrl/danh-sach?type=$vsmovType&page=$page',
      '$phim4kUrl/films/danh-sach/$slug?page=$page',
      '$free1Url/danh-sach/$slug?page=$page',
      '/movies?page=$page&filterType=danh-sach&filterValue=$slug',
      () => MotchillScraper.getByList(slug, page),
      null,
      null,
    );
  }

  static Future<List<Movie>> getMoviesByGenre(
    String slug, {
    int page = 1,
  }) async {
    return _fetchAndMerge(
      '$nguoncUrl/films/the-loai/$slug?page=$page',
      '$kkphimUrl/the-loai/$slug?page=$page',
      '$ophimUrl/the-loai/$slug?page=$page',
      '$vsmovUrl/the-loai/$slug?page=$page',
      '$phim4kUrl/films/the-loai/$slug?page=$page',
      '$free1Url/the-loai/$slug?page=$page',
      '/movies?page=$page&filterType=the-loai&filterValue=$slug',
      () => MotchillScraper.getByGenre(slug, page),
      null,
      null,
    );
  }

  static Future<List<Movie>> getMoviesByCountry(
    String slug, {
    int page = 1,
  }) async {
    return _fetchAndMerge(
      '$nguoncUrl/films/quoc-gia/$slug?page=$page',
      '$kkphimUrl/quoc-gia/$slug?page=$page',
      '$ophimUrl/quoc-gia/$slug?page=$page',
      '$vsmovUrl/quoc-gia/$slug?page=$page',
      '$phim4kUrl/films/quoc-gia/$slug?page=$page',
      '$free1Url/quoc-gia/$slug?page=$page',
      '/movies?page=$page&filterType=quoc-gia&filterValue=$slug',
      () => MotchillScraper.getByCountry(slug, page),
      null,
      null,
    );
  }

  static Future<List<Movie>> searchMovies(String keyword) async {
    final enc = Uri.encodeComponent(keyword);
    return _fetchAndMerge(
      '$nguoncUrl/films/search?keyword=$enc',
      '$kkphimUrl/tim-kiem?keyword=$enc',
      '$ophimUrl/tim-kiem?keyword=$enc',
      '$vsmovUrl/tim-kiem?keyword=$enc',
      '$phim4kUrl/films/search?keyword=$enc',
      '$free1Url/tim-kiem?keyword=$enc',
      '/movies?keyword=$enc',
      () => MotchillScraper.search(keyword),
      () => CinemetaApi.searchCinemeta(keyword),
      () => Film4kNetApi.search(keyword),
    );
  }

  // --- Detail Fetching ---
  static String _processM3u8Url(String url) {
    if (url.isEmpty) return url;
    if (url.contains('workers.dev') ||
        (url.contains('dpdns.org') && !url.contains('stream/hls'))) {
      final rawId = url.split('/').last;

      // TODO: Các server cũ đa phần bị 404 (Cloudflare xoá). Giữ lại ở đây để fix sau.
      /*
      final workers = [
        'demo.cryboiz.workers.dev',
        'sv1.gboiz.workers.dev',
        'sv1.gboiz2.workers.dev',
        'sv.phim4k.dpdns.org',
      ];
      for (int i = 3; i <= 35; i++) {
        workers.add('sv.gboiz$i.workers.dev');
      }
      workers.shuffle();
      return 'https://${workers.first}/$rawId';
      */

      final activeServers = ['sv.gboiz7.workers.dev', 'sv1.p4k.dpdns.org'];
      activeServers.shuffle();
      return 'https://${activeServers.first}/$rawId';
    }
    return url;
  }

  static List<EpisodeServer> _parseEpisodes(List rawEps, String prefix) {
    List<EpisodeServer> servers = [];
    for (var srv in rawEps) {
      String rawName = srv['server_name'] ?? 'Server';
      rawName = rawName.replaceAll(RegExp(r'#\d+|\s+\d+$'), '').trim();
      final serverName = prefix.isNotEmpty ? '$prefix - $rawName' : rawName;

      List epItems = [];
      if (srv['server_data'] is List) {
        epItems = srv['server_data'];
      } else if (srv['items'] is List) {
        epItems = srv['items'];
      }

      final episodes = epItems.map((ep) {
        String rawUrl = (ep['link_m3u8'] ?? ep['m3u8'] ?? ep['link'] ?? '')
            .toString();
        return Episode(
          name: (ep['name'] ?? '').toString(),
          slug: (ep['slug'] ?? '').toString(),
          m3u8Url: _processM3u8Url(rawUrl),
          embedUrl: (ep['link_embed'] ?? ep['embed'] ?? '').toString(),
        );
      }).toList();
      servers.add(EpisodeServer(serverName: serverName, items: episodes));
    }
    return servers;
  }

  static bool _isSimilarMovieGlobal(Movie? initial, Movie fetched) {
    if (initial == null) return true;
    if (initial.originalName.isNotEmpty && fetched.originalName.isNotEmpty) {
      String normA = initial.originalName.toLowerCase().replaceAll(
        RegExp(r'[^a-z0-9]'),
        '',
      );
      String normB = fetched.originalName.toLowerCase().replaceAll(
        RegExp(r'[^a-z0-9]'),
        '',
      );
      if (normA != normB && !normA.contains(normB) && !normB.contains(normA)) {
        return false;
      }
    }
    if (initial.year.isNotEmpty &&
        fetched.year.isNotEmpty &&
        initial.year != fetched.year) {
      return false;
    }
    return true;
  }


  static String _slugify(String text) {
    String lower = text.toLowerCase().trim();
    lower = lower.replaceAll(RegExp(r'[^a-z0-9\s]'), '');
    return lower.replaceAll(RegExp(r'\s+'), '-');
  }

  static Stream<Movie> fetchMovieDetailStream(

    String slug, {
    Movie? initialMovie,
  }) {
    final controller = StreamController<Movie>();
    final Map<int, Movie> parsedMap = {};
    final Map<int, List<EpisodeServer>> serversMap = {};

    void processAndEmit() {
      if (parsedMap.isEmpty) return;

      final order = [6, 3, 7, 1, 0, 2, 4, 5, 10, 8, 9];

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
        
        bool mergedHasBackdrop = merged.posterUrl.isNotEmpty && merged.posterUrl != merged.thumbUrl;
        bool itemHasBackdrop = item.posterUrl.isNotEmpty && item.posterUrl != item.thumbUrl;
        String bestPosterUrl = mergedHasBackdrop 
            ? merged.posterUrl 
            : (itemHasBackdrop ? item.posterUrl : (merged.posterUrl.isNotEmpty ? merged.posterUrl : item.posterUrl));

        merged = merged.copyWith(
          thumbUrl: merged.thumbUrl.isNotEmpty ? merged.thumbUrl : item.thumbUrl,
          posterUrl: bestPosterUrl,
          currentEpisode:
              (merged.currentEpisode.isNotEmpty &&
                  merged.currentEpisode != 'Đang cập nhật' &&
                  merged.currentEpisode != 'N/A')
              ? merged.currentEpisode
              : item.currentEpisode,
          quality:
              (merged.quality.isNotEmpty &&
                  merged.quality != 'N/A')
              ? merged.quality
              : item.quality,
          time: (merged.time.isNotEmpty && merged.time != 'N/A')
              ? merged.time
              : item.time,
          language:
              (merged.language.isNotEmpty &&
                  merged.language != 'N/A')
              ? merged.language
              : item.language,
          description: merged.description.isNotEmpty
              ? merged.description
              : item.description,
          year: merged.year.isNotEmpty ? merged.year : item.year,
          genres: merged.genres.isNotEmpty ? merged.genres : item.genres,
          countries: merged.countries.isNotEmpty ? merged.countries : item.countries,
          directors: merged.directors.isNotEmpty ? merged.directors : item.directors,
          casts: merged.casts.isNotEmpty ? merged.casts : item.casts,
          source: merged.source != item.source ? 'mixed' : merged.source,
        );
      }

      merged = merged.copyWith(
        episodes: allServers
            .where(
              (server) => server.items.any(
                (ep) => ep.m3u8Url.isNotEmpty || ep.embedUrl.isNotEmpty,
              ),
            )
            .toList(),
      );

      controller.add(merged);
    }

    SharedPreferences.getInstance().then((prefs) {
      final enabledSources =
          prefs.getStringList('enabled_sources') ??
          [
            'premium',
            'nguonc',
            'ophim',
            'kkphim',
            'vsmov',
            'film4knet',
            'phim4k',
            'free1',
            'motchill',
          ];
      final timeout = const Duration(seconds: 5);
      final List<Future> futures = [];

      if (enabledSources.contains('film4knet')) {
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
      }

      if (enabledSources.contains('nguonc')) {
        final querySlug = initialMovie?.sourceSlugs['nguonc'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$nguoncUrl/film/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = data['movie'] ?? data['item'];
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizeNguonC(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[0] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? dataItem['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[0] = _parseEpisodes(
                      epsList as List? ?? [],
                      'NguonC',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('kkphim')) {
        final querySlug = initialMovie?.sourceSlugs['kkphim'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$kkphimUrl/phim/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = (data['movie'] != null)
                      ? data['movie']
                      : (data['data'] != null ? data['data']['item'] : null);
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizeKKPhim(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[1] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? dataItem['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[1] = _parseEpisodes(
                      epsList as List? ?? [],
                      'KKPhim',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('ophim')) {
        final querySlug = initialMovie?.sourceSlugs['ophim'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$ophimUrl/phim/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = (data['data'] != null)
                      ? (data['data']['item'] ?? data['data']['movie'])
                      : (data['movie'] ?? data['item']);
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizeOphim(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[7] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? dataItem['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[7] = _parseEpisodes(
                      epsList as List? ?? [],
                      'Ophim',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('phim4k')) {
        final querySlug = initialMovie?.sourceSlugs['phim4k'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$phim4kUrl/film/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = data['movie'] ?? data['item'];
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizePhim4K(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[2] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? dataItem['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[2] = _parseEpisodes(
                      epsList as List? ?? [],
                      'Free2',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('vsmov')) {
        final querySlug = initialMovie?.sourceSlugs['vsmov'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$vsmovUrl/phim/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = data['movie'] ?? data['item'];
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizeVSMov(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[3] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? dataItem['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[3] = _parseEpisodes(
                      epsList as List? ?? [],
                      'VSMov',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('free1')) {
        final querySlug = initialMovie?.sourceSlugs['free1'] ?? slug;
        futures.add(
          http
              .get(Uri.parse('$free1Url/phim/$querySlug'))
              .timeout(timeout)
              .then((res) {
                if (res.statusCode == 200) {
                  final data = json.decode(res.body);
                  final movieData = (data['data'] != null)
                      ? data['data']['item']
                      : (data['movie'] ?? data['item']);
                  if (movieData != null) {
                    Movie fetchedMovie = _normalizeFree1(movieData);
                    if (!_isSimilarMovieGlobal(initialMovie, fetchedMovie))
                      return;

                    parsedMap[4] = fetchedMovie;
                    var dataItem = data['data'] != null
                        ? data['data']['item']
                        : null;
                    var epsList =
                        (dataItem != null ? data['data']['episodes'] : null) ??
                        data['episodes'] ??
                        data['episode'] ??
                        movieData['episodes'] ??
                        movieData['episode'];
                    serversMap[4] = _parseEpisodes(
                      epsList as List? ?? [],
                      'Free1',
                    );
                    processAndEmit();
                  }
                }
              })
              .catchError((_) {}),
        );
      }

      if (enabledSources.contains('premium')) {
        Future<void> fetchPremium() async {
          // Helper: slug word overlap check (same as web version)
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

          print(
            '[Premium DEBUG] slug=$slug, querySlug=$querySlug, initialMovie sourceSlugs=${initialMovie?.sourceSlugs}',
          );

          // 1. Try with provided slug directly
          try {
            final res = await http
                .get(
                  Uri.parse(
                    'https://dogtail.oxaliplatin.workers.dev/api/premium/detail/$querySlug',
                  ),
                )
                .timeout(timeout);
            if (res.statusCode == 200) {
              final data = json.decode(res.body);
              if (data['movie'] != null || data['item'] != null) {
                movieData = data['movie'] ?? data['item'];

                // If episodes are empty and we used a premium-ID slug, try with the original slug
                final eps = movieData!['episodes'];
                final hasEmptyEps =
                    eps == null ||
                    (eps is List &&
                        (eps.isEmpty ||
                            eps.every((srv) {
                              final sd = srv['server_data'];
                              return sd == null || (sd is List && sd.isEmpty);
                            })));

                if (hasEmptyEps && querySlug.startsWith('premium-')) {
                  // Try the saved original slug from the list (stored when normalizing premium items)
                  String originalSlug =
                      initialMovie?.sourceSlugs['premium_original'] ?? '';
                  print(
                    '[Premium DEBUG] hasEmptyEps=true, originalSlug from sourceSlugs: "$originalSlug"',
                  );

                  // If not available, search by the movie name we got from the API response
                  if (originalSlug.isEmpty ||
                      originalSlug.startsWith('premium-')) {
                    final movieName =
                        (movieData!['name'] ?? movieData!['origin_name'] ?? '')
                            .toString();
                    final movieSlug = (movieData!['slug'] ?? '').toString();
                    // Use the slug from movieData if it's not a premium-ID format
                    if (movieSlug.isNotEmpty &&
                        !movieSlug.startsWith('premium-')) {
                      originalSlug = movieSlug;
                      print(
                        '[Premium DEBUG] Using slug from movieData response: "$originalSlug"',
                      );
                    } else if (movieName.isNotEmpty) {
                      // Search by name to find the right slug
                      final keyword = movieName.split(' ').take(5).join(' ');
                      print(
                        '[Premium DEBUG] Searching premium by name: "$keyword"',
                      );
                      try {
                        final searchRes = await http
                            .get(
                              Uri.parse(
                                'https://dogtail.oxaliplatin.workers.dev/api/premium/movies?keyword=${Uri.encodeComponent(keyword)}',
                              ),
                            )
                            .timeout(const Duration(seconds: 5));
                        if (searchRes.statusCode == 200) {
                          final searchData = json.decode(searchRes.body);
                          final items = (searchData['items'] as List?) ?? [];
                          for (var item in items) {
                            if (item is Map<String, dynamic>) {
                              final itemSlug = (item['slug'] ?? '').toString();
                              if (itemSlug.isNotEmpty &&
                                  !itemSlug.startsWith('premium-')) {
                                originalSlug = itemSlug;
                                print(
                                  '[Premium DEBUG] Found original slug via search: "$originalSlug"',
                                );
                                break;
                              }
                            }
                          }
                        }
                      } catch (e) {}
                    }
                  }

                  if (originalSlug.isNotEmpty &&
                      originalSlug != querySlug &&
                      !originalSlug.startsWith('premium-')) {
                    print(
                      '[Premium DEBUG] Refetching with original slug: $originalSlug',
                    );
                    try {
                      final res2 = await http
                          .get(
                            Uri.parse(
                              'https://dogtail.oxaliplatin.workers.dev/api/premium/detail/$originalSlug',
                            ),
                          )
                          .timeout(timeout);
                      if (res2.statusCode == 200) {
                        final data2 = json.decode(res2.body);
                        final d2 = data2['movie'] ?? data2['item'];
                        if (d2 != null) {
                          final eps2 = d2['episodes'];
                          final hasEps2 =
                              eps2 is List &&
                              eps2.isNotEmpty &&
                              eps2.any((srv) {
                                final sd = srv['server_data'];
                                return sd is List && sd.isNotEmpty;
                              });
                          if (hasEps2) {
                            print(
                              '[Premium DEBUG] Refetch successful with $originalSlug, episodes found!',
                            );
                            movieData = d2;
                          }
                        }
                      }
                    } catch (e) {}
                  }
                }
              }
            }
          } catch (e) {}

          // 2. If not found, try slug variations (like the web version)
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
                  final res = await http
                      .get(
                        Uri.parse(
                          'https://dogtail.oxaliplatin.workers.dev/api/premium/detail/$v',
                        ),
                      )
                      .timeout(const Duration(seconds: 5));
                  if (res.statusCode == 200) {
                    final data = json.decode(res.body);
                    if (data['movie'] != null || data['item'] != null) {
                      movieData = data['movie'] ?? data['item'];
                      break;
                    }
                  }
                } catch (e) {}
              }
            }
          }

          // 3. If still not found, search by keyword with slug word overlap (like web version)
          if (movieData == null && !querySlug.startsWith('premium-')) {
            final words = slug.split('-');
            final keywords = [
              slug.replaceAll('-', ' '),
              words.isNotEmpty ? words[0] : '',
              words.length > 1 ? words.skip(1).join(' ') : '',
            ].where((kw) => kw.length > 2).toSet().toList();

            for (var kw in keywords) {
              try {
                final searchUrl =
                    'https://dogtail.oxaliplatin.workers.dev/api/premium/movies?keyword=${Uri.encodeComponent(kw)}';
                final res = await http
                    .get(Uri.parse(searchUrl))
                    .timeout(const Duration(seconds: 6));
                if (res.statusCode == 200) {
                  final searchData = json.decode(res.body);
                  final items = (searchData['items'] as List?) ?? [];
                  Map<String, dynamic>? bestMatch;

                  for (var item in items) {
                    if (item is! Map<String, dynamic>) continue;
                    final itemSlug = (item['slug'] ?? '').toString();
                    // Use slug word overlap (same as web version)
                    if (slugMatches(itemSlug)) {
                      bestMatch = item;
                      break;
                    }
                    // Also check if initialMovie name matches
                    if (initialMovie != null &&
                        _isSimilarMovieGlobal(
                          initialMovie,
                          Movie.fromJson(item, defaultSource: 'premium'),
                        )) {
                      bestMatch = item;
                      break;
                    }
                  }

                  if (bestMatch != null) {
                    final bestSlug = (bestMatch['slug'] ?? '').toString();
                    // If slug matches, use it directly
                    Map<String, dynamic>? detailData;
                    if (bestSlug != slug) {
                      try {
                        final detailRes = await http
                            .get(
                              Uri.parse(
                                'https://dogtail.oxaliplatin.workers.dev/api/premium/detail/$bestSlug',
                              ),
                            )
                            .timeout(const Duration(seconds: 6));
                        if (detailRes.statusCode == 200) {
                          final dd = json.decode(detailRes.body);
                          if (dd['movie'] != null || dd['item'] != null) {
                            detailData = dd;
                          }
                        }
                      } catch (e) {}
                    }
                    // Also try with premium-type-id format
                    if (detailData == null) {
                      final type = bestMatch['type'] == 'series'
                          ? 'series'
                          : 'movie';
                      final id = bestMatch['raw_payload'] ?? bestMatch['_id'];
                      if (id != null) {
                        try {
                          final matchedUrl =
                              'https://dogtail.oxaliplatin.workers.dev/api/premium/detail/premium-$type-$id';
                          final detailRes = await http
                              .get(Uri.parse(matchedUrl))
                              .timeout(const Duration(seconds: 6));
                          if (detailRes.statusCode == 200) {
                            final dd = json.decode(detailRes.body);
                            if (dd['movie'] != null || dd['item'] != null) {
                              detailData = dd;
                            }
                          }
                        } catch (e) {}
                      }
                    }
                    if (detailData != null) {
                      movieData = detailData['movie'] ?? detailData['item'];
                      break;
                    }
                  }
                }
              } catch (e) {}
              if (movieData != null) break;
            }
          }

          if (movieData != null) {
            var m = Movie.fromJson(
              movieData as Map<String, dynamic>,
              defaultSource: 'premium',
            ).copyWith(quality: 'Premium');
            // Don't reject if _isSimilarMovieGlobal returns false due to missing data — we already matched by slug overlap
            parsedMap[5] = m;

            List<EpisodeServer> premiumServers = [];
            final rawEpisodes = movieData['episodes'];
            print(
              '[Premium DEBUG] movieData keys: ${(movieData as Map).keys.toList()}',
            );
            print(
              '[Premium DEBUG] rawEpisodes type: ${rawEpisodes?.runtimeType}, value: $rawEpisodes',
            );
            final premEps = (rawEpisodes is List) ? rawEpisodes : [];
            print('[Premium DEBUG] premEps count: ${premEps.length}');
            for (var srv in premEps) {
              print(
                '[Premium DEBUG] srv type: ${srv.runtimeType}, keys: ${(srv as Map).keys.toList()}',
              );
              final serverName = (srv['server_name'] ?? 'Premium Server')
                  .toString();
              final serverData = srv['server_data'];
              final serverItems = srv['items'];
              print(
                '[Premium DEBUG] server_data type: ${serverData?.runtimeType}, items type: ${serverItems?.runtimeType}',
              );
              List epItems = (serverData is List)
                  ? serverData
                  : ((serverItems is List) ? serverItems : []);
              print('[Premium DEBUG] epItems count: ${epItems.length}');
              final episodes = epItems.map((ep) {
                final link = (ep['link'] ?? ep['link_m3u8'] ?? '').toString();
                final processed = _processM3u8Url(link);
                print(
                  '[Premium DEBUG] ep name: ${ep['name']}, link: $link, processed: $processed',
                );
                return Episode(
                  name: (ep['name'] ?? '').toString(),
                  slug: (ep['slug'] ?? '').toString(),
                  m3u8Url: processed,
                  embedUrl: (ep['link_embed'] ?? ep['embed'] ?? '').toString(),
                );
              }).toList();
              premiumServers.add(
                EpisodeServer(serverName: serverName, items: episodes),
              );
            }
            print(
              '[Premium DEBUG] premiumServers count: ${premiumServers.length}',
            );
            serversMap[5] = premiumServers;
            processAndEmit();
          }
        }

        futures.add(fetchPremium());
      }

      if (enabledSources.contains('motchill')) {
        final querySlug = initialMovie?.sourceSlugs['motchill'] ?? slug;
        futures.add(
          MotchillScraper.getDetail(querySlug)
              .timeout(timeout)
              .then((motchillData) {
                if (motchillData != null) {
                  if (!_isSimilarMovieGlobal(initialMovie, motchillData))
                    return;

                  parsedMap[6] = motchillData;
                  serversMap[6] = motchillData.episodes;
                  processAndEmit();
                }
              })
              .catchError((_) {}),
        );
      } // Added missing brace

      if (initialMovie != null &&
          (initialMovie.imdbId == null ||
              initialMovie.imdbId!.isEmpty ||
              initialMovie.imdbId == 'N/A')) {
        futures.add(() async {
          try {
            final isTv =
                initialMovie.type.toLowerCase() == 'series' ||
                initialMovie.type.toLowerCase() == 'tvshows' ||
                initialMovie.currentEpisode.toLowerCase().contains('tập') ||
                initialMovie.currentEpisode.contains('/') ||
                initialMovie.time.toLowerCase().contains('tập') ||
                initialMovie.episodes.any((e) => e.items.length > 1);

            final id = await TorrentioApi.getImdbId(
              initialMovie.name,
              initialMovie.originalName,
              initialMovie.year,
              isTv,
            );
            if (id != null && id.isNotEmpty) {
              if (parsedMap.isNotEmpty) {
                for (var key in parsedMap.keys) {
                  parsedMap[key] = parsedMap[key]!.copyWith(imdbId: id);
                }
                processAndEmit();
              }
            }
          } catch (_) {}
        }());
      }

      if ((enabledSources.contains('torrentio') ||
              enabledSources.contains('vidsrc') ||
              enabledSources.contains('vidapi')) &&
          initialMovie != null) {
        futures.add(() async {
          try {
            String imdbId =
                initialMovie.sourceSlugs['torrentio'] ??
                initialMovie.sourceSlugs['stremio'] ??
                '';
            final isTv =
                initialMovie.type.toLowerCase() == 'series' ||
                initialMovie.type.toLowerCase() == 'tvshows' ||
                initialMovie.currentEpisode.toLowerCase().contains('tập') ||
                initialMovie.currentEpisode.contains('/') ||
                initialMovie.time.toLowerCase().contains('tập') ||
                initialMovie.episodes.any((e) => e.items.length > 1);

            if (initialMovie.source == 'stremio' && imdbId.isNotEmpty) {
              // Fetch full metadata from Cinemeta
              final meta = await CinemetaApi.getMetaDetail(
                imdbId,
                isSeries: isTv,
              );
              if (meta != null) {
                parsedMap[8] = meta; // Use index 8 for stremio meta
                processAndEmit();
              }
            }

            if (imdbId.isEmpty &&
                initialMovie.imdbId != null &&
                initialMovie.imdbId!.isNotEmpty) {
              imdbId = initialMovie.imdbId!;
            }

            if (imdbId.isEmpty) {
              final id = await TorrentioApi.getImdbId(
                initialMovie.name,
                initialMovie.originalName,
                initialMovie.year,
                isTv,
              );
              if (id != null) imdbId = id;
            }

            if (imdbId.isNotEmpty) {
              // Update the initial movie with the found IMDB ID so UI can use it
              if (parsedMap.isNotEmpty) {
                final firstKey = parsedMap.keys.first;
                parsedMap[firstKey] = parsedMap[firstKey]!.copyWith(
                  imdbId: imdbId,
                );
              }

              final tmdbId = await TorrentioApi.getTmdbIdFromImdb(imdbId);

              // Check if it's a TV show, if so we don't fetch streams here, we just emit the imdbId
              // and fetch the episodes list from Cinemeta
              if (isTv) {
                final cinemetaEpisodes = await CinemetaApi.getSeriesEpisodes(
                  imdbId,
                );
                if (cinemetaEpisodes.isNotEmpty) {
                  final p2pItems = cinemetaEpisodes
                      .map(
                        (e) => Episode(
                          name: 'Tập ${e['episode']}',
                          slug: 'S${e['season']}E${e['episode']}',
                          m3u8Url:
                              'torrentio://$imdbId:${e['season']}:${e['episode']}',
                          embedUrl: '',
                        ),
                      )
                      .toList();

                  final vidsrcItems = tmdbId != null
                      ? cinemetaEpisodes
                            .map(
                              (e) => Episode(
                                name: 'Tập ${e['episode']}',
                                slug: 'S${e['season']}E${e['episode']}',
                                m3u8Url: '',
                                embedUrl:
                                    'https://vidsrc.sbs/embed/tv/$tmdbId/${e['season']}/${e['episode']}',
                              ),
                            )
                            .toList()
                      : <Episode>[];

                  final vidApiItems = cinemetaEpisodes
                      .map(
                        (e) => Episode(
                          name: 'Tập ${e['episode']}',
                          slug: 'S${e['season']}E${e['episode']}',
                          m3u8Url: '',
                          embedUrl:
                              'https://vaplayer.ru/embed/tv/$imdbId/${e['season']}/${e['episode']}',
                        ),
                      )
                      .toList();

                  serversMap[9] = [
                    EpisodeServer(serverName: 'P2P (Torrent)', items: p2pItems),
                    if (vidsrcItems.isNotEmpty)
                      EpisodeServer(
                        serverName: 'VidSrc (Embed)',
                        items: vidsrcItems,
                      ),
                    EpisodeServer(
                      serverName: 'VidAPI (Embed)',
                      items: vidApiItems,
                    ),
                  ];
                }
                processAndEmit();
                return;
              }

              final servers = enabledSources.contains('torrentio')
                  ? await TorrentioApi.fetchStreams(imdbId)
                  : <EpisodeServer>[];

              final vidsrcServer =
                  (tmdbId != null && enabledSources.contains('vidsrc'))
                  ? EpisodeServer(
                      serverName: 'VidSrc (Embed)',
                      items: [
                        Episode(
                          name: 'Full',
                          slug: 'full',
                          m3u8Url: '',
                          embedUrl: 'https://vidsrc.sbs/embed/movie/$tmdbId',
                        ),
                      ],
                    )
                  : null;

              final vidApiServer = enabledSources.contains('vidapi')
                  ? EpisodeServer(
                      serverName: 'VidAPI (Embed)',
                      items: [
                        Episode(
                          name: 'Full',
                          slug: 'full',
                          m3u8Url: '',
                          embedUrl: 'https://vaplayer.ru/embed/movie/$imdbId',
                        ),
                      ],
                    )
                  : null;

              if (servers.isNotEmpty) {
                if (vidsrcServer != null) servers.add(vidsrcServer);
                if (vidApiServer != null)
                  servers.add(vidApiServer as EpisodeServer);
                serversMap[9] = servers;
                processAndEmit();
              } else {
                serversMap[9] = [
                  if (vidsrcServer != null) vidsrcServer,
                  if (vidApiServer != null) vidApiServer,
                ];
                processAndEmit();
              }
            }
          } catch (e) {
            print('PhimApi torrentio error: $e');
          }
        }());
      }

      Future.wait(futures)
          .then((_) {
            processAndEmit();
            controller.close();
          })
          .catchError((_) {
            controller.close();
          });
    });

    return controller.stream;
  }

  static const String _tmdbApiKey = 'e9e9d8da18ae29fc430845952232787c';

  static Future<Map<String, dynamic>?> _searchTmdb(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    String type = isTvSeries ? 'tv' : 'movie';
    final query = Uri.encodeComponent(
      originalTitle.isNotEmpty ? originalTitle : title,
    );
    final searchUrl =
        'https://api.themoviedb.org/3/search/multi?query=$query&api_key=$_tmdbApiKey&language=vi-VN';

    try {
      final res = await http.get(Uri.parse(searchUrl));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        if (data['results'] != null && data['results'].isNotEmpty) {
          var match = data['results'][0];
          if (year.isNotEmpty) {
            final yMatch = data['results'].firstWhere(
              (r) => (r['release_date'] ?? r['first_air_date'] ?? '')
                  .toString()
                  .startsWith(year),
              orElse: () => null,
            );
            if (yMatch != null) match = yMatch;
          }
          return {
            'id': match['id']?.toString(),
            'type': match['media_type'] ?? type,
            'tmdbRating': match['vote_average']?.toString(),
            'backdrop_path': match['backdrop_path'],
          };
        }
      }
    } catch (e) {
      print('PhimApi _searchTmdb error: $e');
    }
    return null;
  }

  static Future<List<String>> getMovieImages(Movie movie) async {
    try {
      String? tmdbId;
      String type = (movie.type == 'series' || movie.type == 'hoathinh')
          ? 'tv'
          : 'movie';

      // 1. Cố gắng tìm bằng IMDB ID trước nếu có (chính xác nhất)
      if (movie.imdbId != null &&
          movie.imdbId!.isNotEmpty &&
          movie.imdbId != 'N/A') {
        final findUrl =
            'https://api.themoviedb.org/3/find/${movie.imdbId}?external_source=imdb_id&api_key=$_tmdbApiKey';
        final findRes = await http
            .get(Uri.parse(findUrl))
            .timeout(const Duration(seconds: 10));
        if (findRes.statusCode == 200) {
          final findData = json.decode(findRes.body);
          if (findData['movie_results'] != null &&
              findData['movie_results'].isNotEmpty) {
            tmdbId = findData['movie_results'][0]['id'].toString();
            type = 'movie';
          } else if (findData['tv_results'] != null &&
              findData['tv_results'].isNotEmpty) {
            tmdbId = findData['tv_results'][0]['id'].toString();
            type = 'tv';
          }
        }
      }

      // 2. Nếu không có hoặc không tìm thấy, dùng searchTmdb
      if (tmdbId == null) {
        final match = await _searchTmdb(
          movie.name,
          movie.originalName,
          movie.year,
          movie.type == 'series' || movie.type == 'hoathinh',
        );
        if (match != null && match['id'] != null) {
          tmdbId = match['id'].toString();
          type = match['type'] ?? type;
        }
      }

      // 3. Lấy ảnh từ TMDB
      if (tmdbId != null) {
        final imgUrl =
            'https://api.themoviedb.org/3/$type/$tmdbId/images?api_key=$_tmdbApiKey';
        final imgRes = await http
            .get(Uri.parse(imgUrl))
            .timeout(const Duration(seconds: 10));
        if (imgRes.statusCode == 200) {
          final imgData = json.decode(imgRes.body);
          List<String> imageUrls = [];

          if (imgData['backdrops'] != null) {
            final backdrops = imgData['backdrops'] as List;
            imageUrls.addAll(
              backdrops
                  .take(20)
                  .map(
                    (e) =>
                        'https://image.tmdb.org/t/p/original${e['file_path']}',
                  ),
            );
          }
          if (imgData['posters'] != null) {
            final posters = imgData['posters'] as List;
            imageUrls.addAll(
              posters
                  .take(10)
                  .map(
                    (e) =>
                        'https://image.tmdb.org/t/p/original${e['file_path']}',
                  ),
            );
          }

          return imageUrls;
        }
      }
    } catch (e) {
      print('PhimApi getMovieImages error: $e');
    }
    return [];
  }

  static Future<String?> getMovieTmdbBackdrop(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    final match = await _searchTmdb(title, originalTitle, year, isTvSeries);
    if (match != null && match['backdrop_path'] != null) {
      return 'https://image.tmdb.org/t/p/w1280${match['backdrop_path']}';
    }
    return null;
  }

  static Future<String?> getMovieTmdbRating(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    final match = await _searchTmdb(title, originalTitle, year, isTvSeries);
    return match?['tmdbRating'];
  }

  static Future<List<Map<String, String>>> getMovieActors(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    try {
      final match = await _searchTmdb(title, originalTitle, year, isTvSeries);
      if (match != null && match['id'] != null) {
        final creditsUrl =
            'https://api.themoviedb.org/3/${match['type']}/${match['id']}/credits?api_key=$_tmdbApiKey&language=vi-VN';
        final res = await http.get(Uri.parse(creditsUrl));
        if (res.statusCode == 200) {
          final data = json.decode(res.body);
          final casts = data['cast'] as List?;
          if (casts != null) {
            return casts.take(15).map((c) {
              return {
                'id': c['id']?.toString() ?? '',
                'name': c['name']?.toString() ?? '',
                'character': c['character']?.toString() ?? '',
                'profile': c['profile_path'] != null
                    ? 'https://image.tmdb.org/t/p/w200${c['profile_path']}'
                    : '',
              };
            }).toList();
          }
        }
      }
    } catch (e) {
      print('PhimApi getMovieActors error: $e');
    }
    return [];
  }

  static Future<String?> getTrailerStreamUrl(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    try {
      final match = await _searchTmdb(title, originalTitle, year, isTvSeries);
      if (match != null && match['id'] != null) {
        final videoUrl =
            'https://api.themoviedb.org/3/${match['type']}/${match['id']}/videos?api_key=$_tmdbApiKey';
        final videoRes = await http.get(Uri.parse(videoUrl));
        if (videoRes.statusCode == 200) {
          final videoData = json.decode(videoRes.body);
          if (videoData['results'] != null && videoData['results'].isNotEmpty) {
            final List results = videoData['results'];
            var trailer = results.firstWhere(
              (v) => v['site'] == 'YouTube' && v['type'] == 'Trailer',
              orElse: () => null,
            );
            trailer ??= results.firstWhere(
              (v) => v['site'] == 'YouTube',
              orElse: () => null,
            );

            if (trailer != null) {
              return trailer['key'];
            }
          }
        }
      }
    } catch (e) {
      print('PhimApi TMDB getTrailerStreamUrl error: $e');
    }

    // Fallback: Tìm kiếm trực tiếp trên YouTube bằng tên gốc (Original Title) + "trailer"
    try {
      final query = Uri.encodeComponent('$originalTitle trailer');
      final ytUrl = Uri.parse(
        'https://www.youtube.com/results?search_query=$query',
      );
      final ytRes = await http.get(
        ytUrl,
        headers: {
          'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
      );

      if (ytRes.statusCode == 200) {
        final regex = RegExp(r'/watch\?v=([a-zA-Z0-9_-]{11})');
        final match = regex.firstMatch(ytRes.body);
        if (match != null && match.group(1) != null) {
          return match.group(1);
        }
      }
    } catch (e) {
      print('PhimApi YouTube scrape error: $e');
    }

    return null;
  }

  static Future<Map<String, dynamic>?> getActorDetails(String personId) async {
    try {
      final url =
          'https://api.themoviedb.org/3/person/$personId?api_key=$_tmdbApiKey&language=vi-VN';
      final res = await http.get(Uri.parse(url));
      if (res.statusCode == 200) {
        return json.decode(res.body);
      }
    } catch (e) {
      print('PhimApi getActorDetails error: $e');
    }
    return null;
  }

  static Future<List<Map<String, dynamic>>> getActorMovieCredits(
    String personId,
  ) async {
    try {
      final url =
          'https://api.themoviedb.org/3/person/$personId/movie_credits?api_key=$_tmdbApiKey&language=vi-VN';
      final res = await http.get(Uri.parse(url));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final cast = data['cast'] as List?;
        if (cast != null) {
          final filtered = cast.where((m) => m['poster_path'] != null).toList();
          filtered.sort(
            (a, b) => (b['popularity'] as num? ?? 0).compareTo(
              a['popularity'] as num? ?? 0,
            ),
          );
          return filtered.cast<Map<String, dynamic>>();
        }
      }
    } catch (e) {
      print('PhimApi getActorMovieCredits error: $e');
    }
    return [];
  }
}
tmdbApiKey';
        final res = await http.get(Uri.parse(imgUrl));
        if (res.statusCode == 200) {
          final data = json.decode(res.body);
          if (data['logos'] != null && (data['logos'] as List).isNotEmpty) {
            final List logos = data['logos'];
            var targetLogo = logos.firstWhere(
                (l) => l['iso_639_1'] == language,
                orElse: () => null);
            if (targetLogo != null) {
              return 'https://image.tmdb.org/t/p/w500${targetLogo['file_path']}';
            }
          }
        }
      }
    } catch (e) {
      print('PhimApi TMDB getMovieTmdbLogo error: $e');
    }
    return null;
  }

  static Future<String?> getMovieTmdbBackdrop(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    final match = await _searchTmdb(title, originalTitle, year, isTvSeries);
    if (match != null && match['backdrop_path'] != null) {
      return 'https://image.tmdb.org/t/p/w1280${match['backdrop_path']}';
    }
    return null;
  }

  static Future<String?> getMovieTmdbRating(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    final match = await _searchTmdb(title, originalTitle, year, isTvSeries);
    return match?['tmdbRating'];
  }

  static Future<List<Map<String, String>>> getMovieActors(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    try {
      final match = await _searchTmdb(title, originalTitle, year, isTvSeries);
      if (match != null && match['id'] != null) {
        final creditsUrl =
            'https://api.themoviedb.org/3/${match['type']}/${match['id']}/credits?api_key=$_tmdbApiKey&language=vi-VN';
        final res = await http.get(Uri.parse(creditsUrl));
        if (res.statusCode == 200) {
          final data = json.decode(res.body);
          final casts = data['cast'] as List?;
          if (casts != null) {
            return casts.take(15).map((c) {
              return {
                'id': c['id']?.toString() ?? '',
                'name': c['name']?.toString() ?? '',
                'character': c['character']?.toString() ?? '',
                'profile': c['profile_path'] != null
                    ? 'https://image.tmdb.org/t/p/w200${c['profile_path']}'
                    : '',
              };
            }).toList();
          }
        }
      }
    } catch (e) {
      print('PhimApi getMovieActors error: $e');
    }
    return [];
  }

  static Future<String?> getTrailerStreamUrl(
    String title,
    String originalTitle,
    String year,
    bool isTvSeries,
  ) async {
    try {
      final match = await _searchTmdb(title, originalTitle, year, isTvSeries);
      if (match != null && match['id'] != null) {
        final videoUrl =
            'https://api.themoviedb.org/3/${match['type']}/${match['id']}/videos?api_key=$_tmdbApiKey';
        final videoRes = await http.get(Uri.parse(videoUrl));
        if (videoRes.statusCode == 200) {
          final videoData = json.decode(videoRes.body);
          if (videoData['results'] != null && videoData['results'].isNotEmpty) {
            final List results = videoData['results'];
            var trailer = results.firstWhere(
              (v) => v['site'] == 'YouTube' && v['type'] == 'Trailer',
              orElse: () => null,
            );
            trailer ??= results.firstWhere(
              (v) => v['site'] == 'YouTube',
              orElse: () => null,
            );

            if (trailer != null) {
              return trailer['key'];
            }
          }
        }
      }
    } catch (e) {
      print('PhimApi TMDB getTrailerStreamUrl error: $e');
    }

    // Fallback: Tìm kiếm trực tiếp trên YouTube bằng tên gốc (Original Title) + "trailer"
    try {
      final query = Uri.encodeComponent('$originalTitle trailer');
      final ytUrl = Uri.parse(
        'https://www.youtube.com/results?search_query=$query',
      );
      final ytRes = await http.get(
        ytUrl,
        headers: {
          'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
      );

      if (ytRes.statusCode == 200) {
        final regex = RegExp(r'/watch\?v=([a-zA-Z0-9_-]{11})');
        final match = regex.firstMatch(ytRes.body);
        if (match != null && match.group(1) != null) {
          return match.group(1);
        }
      }
    } catch (e) {
      print('PhimApi YouTube scrape error: $e');
    }

    return null;
  }

  static Future<Map<String, dynamic>?> getActorDetails(String personId) async {
    try {
      final url =
          'https://api.themoviedb.org/3/person/$personId?api_key=$_tmdbApiKey&language=vi-VN';
      final res = await http.get(Uri.parse(url));
      if (res.statusCode == 200) {
        return json.decode(res.body);
      }
    } catch (e) {
      print('PhimApi getActorDetails error: $e');
    }
    return null;
  }

  static Future<List<Map<String, dynamic>>> getActorMovieCredits(
    String personId,
  ) async {
    try {
      final url =
          'https://api.themoviedb.org/3/person/$personId/movie_credits?api_key=$_tmdbApiKey&language=vi-VN';
      final res = await http.get(Uri.parse(url));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final cast = data['cast'] as List?;
        if (cast != null) {
          final filtered = cast.where((m) => m['poster_path'] != null).toList();
          filtered.sort(
            (a, b) => (b['popularity'] as num? ?? 0).compareTo(
              a['popularity'] as num? ?? 0,
            ),
          );
          return filtered.cast<Map<String, dynamic>>();
        }
      }
    } catch (e) {
      print('PhimApi getActorMovieCredits error: $e');
    }
    return [];
  }
}

