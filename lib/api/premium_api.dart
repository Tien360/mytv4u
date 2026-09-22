
import 'dart:convert';
import 'package:http/http.dart' as http;

class PremiumApi {
  static void preload() {
    _fetchMetadata();
  }

  static String? get medataDomain => _medataDomain;
  static String? _apiKey;
  static String? _apiDomain;
  static String? _medataDomain;
  static bool _metadataLoaded = false;
  static Map<String, String> _genresMap = {};
  static Map<String, String> _countriesMap = {};
  
  static final List<String> _fallbackDomains = [
    "https://aa.maclife.dpdns.org",
    "https://apip4k.dpdns.org",
    "https://api.phim4k.lol"
  ];
  
  static const String _apiPath = "/rest-api/v130";
  
  // Clears the cache to force a re-fetch on the next request
  static void clearCache() {
    _apiKey = null;
    _apiDomain = null;
    _metadataLoaded = false;
    print('[PremiumApi] Cache cleared due to failure');
  }

  static Future<void> _initCache() async {
    final client = http.Client();
    
    // Fetch dynamic API KEY
    if (_apiKey == null) {
      try {
        final req = http.Request('GET', Uri.parse('https://rip.cryboiz.workers.dev/go/tokens'))..followRedirects = false;
        final res = await client.send(req).timeout(const Duration(seconds: 5));
        if (res.isRedirect && res.headers['location'] != null) {
          final uri = Uri.parse(res.headers['location']!);
          _apiKey = uri.host;
          print('[PremiumApi] Dynamic API Key: $_apiKey');
        }
      } catch (e) {
        print('[PremiumApi] Failed to fetch API key: $e');
      }
    }
    
    // Fetch dynamic API DOMAIN
    
      if (_medataDomain == null) {
        try {
          final req = http.Request('GET', Uri.parse('https://rip.cryboiz.workers.dev/go/medata'))..followRedirects = false;
          req.headers['User-Agent'] = 'Dart/3.12 (dart:io)';
          final res = await req.send();
          if (res.statusCode == 301 || res.statusCode == 302) {
            final loc = res.headers['location'];
            if (loc != null && loc.isNotEmpty) {
              _medataDomain = loc.endsWith('/') ? loc.substring(0, loc.length - 1) : loc;
            }
          }
        } catch (_) {}
      }

      if (_apiDomain == null) {
      try {
        final req = http.Request('GET', Uri.parse('https://rip.cryboiz.workers.dev/go/api'))..followRedirects = false;
        final res = await client.send(req).timeout(const Duration(seconds: 5));
        if (res.isRedirect && res.headers['location'] != null) {
          String loc = res.headers['location']!;
          if (loc.endsWith('/')) loc = loc.substring(0, loc.length - 1);
          _apiDomain = loc;
          print('[PremiumApi] Dynamic API Domain: $_apiDomain');
        }
      } catch (e) {
        print('[PremiumApi] Failed to fetch API Domain: $e');
      }
    }
    
    if (_apiKey == null) _apiKey = "bbbb411dea44849"; // fallback
  }

  static String _removeAccents(String str) {
    var withDia = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ';
    var withoutDia = 'aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyydAAAAAAAAAAAAAAAAAEEEEEEEEEEEIIIIIOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYD';
    for (int i = 0; i < withDia.length; i++) {
      str = str.replaceAll(withDia[i], withoutDia[i]);
    }
    return str;
  }

  static String _makeSlug(String str) {
    if (str.isEmpty) return "";
    str = _removeAccents(str).toLowerCase();
    str = str.replaceAll(RegExp(r'[^a-z0-9]+'), '-');
    str = str.replaceAll(RegExp(r'^-|-$'), '');
    return str;
  }

  static Map<String, String> _getHeaders() {
    return {
      "API-KEY": _apiKey ?? "bbbb411dea44849",
      "User-Agent": "Dart/3.12 (dart:io)",
      "accept": "application/json"
    };
  }

  static Future<dynamic> _fetchWithFallback(String endpoint) async {
    await _initCache();
    
    List<String> domainsToTry = [];
    if (_apiDomain != null) domainsToTry.add(_apiDomain!);
    for (var d in _fallbackDomains) {
      if (!domainsToTry.contains(d)) domainsToTry.add(d);
    }
    
    Exception? lastError;
    for (final domain in domainsToTry) {
      final url = "$domain$_apiPath$endpoint";
      for (int i = 0; i < 2; i++) {
        try {
          final res = await http.get(Uri.parse(url), headers: _getHeaders()).timeout(const Duration(seconds: 10));
          if (res.statusCode >= 200 && res.statusCode < 300) {
            return json.decode(res.body);
          } else {
             // If Unauthorized or Forbidden, might be invalid key/domain, clear cache
             if (res.statusCode == 401 || res.statusCode == 403) {
                 clearCache();
             }
             throw Exception("HTTP ${res.statusCode}");
          }
        } catch (e) {
          lastError = e is Exception ? e : Exception(e.toString());
          if (i == 1) break;
          await Future.delayed(const Duration(milliseconds: 800));
        }
      }
    }
    throw lastError ?? Exception("All API servers failed");
  }

  static Future<void> _fetchMetadata() async {
    if (_metadataLoaded) return;
    try {
      final genres = await _fetchWithFallback("/all_genre");
      if (genres is List) {
        for (var g in genres) {
          _genresMap[_makeSlug(g['name'] ?? '')] = (g['genre_id'] ?? '').toString();
        }
        if (!_genresMap.containsKey("hoat-hinh")) {
          final hh = genres.firstWhere((g) => (g['name'] ?? '').toString().toLowerCase().contains("hoạt hình"), orElse: () => null);
          _genresMap["hoat-hinh"] = hh != null ? hh['genre_id'].toString() : "10";
        }
      }
    } catch (_) {}

    try {
      final countries = await _fetchWithFallback("/all_country");
      if (countries is List) {
        for (var c in countries) {
          _countriesMap[_makeSlug(c['name'] ?? '')] = (c['country_id'] ?? '').toString();
        }
        if (!_countriesMap.containsKey("au-my")) {
          final am = countries.firstWhere((c) => (c['name'] ?? '').toString().toLowerCase().contains("âu mỹ") || (c['name'] ?? '').toString().toLowerCase().contains("mỹ"), orElse: () => null);
          _countriesMap["au-my"] = am != null ? am['country_id'].toString() : "1";
        }
      }
    } catch (_) {}
    
    _metadataLoaded = true;
  }


  static Future<Map<String, dynamic>> getHomeList(String filterType, String filterValue, int page) async {
    await _fetchMetadata();
    String endpoint = "/movies?page=$page";
    
    if (filterType == "danh-sach") {
        if (filterValue == "phim-le" || filterValue == "phim-chieu-rap") {
            endpoint = "/movies?page=$page";
        } else if (filterValue == "phim-bo" || filterValue == "tv-shows") {
            endpoint = "/tvseries?page=$page";
        } else if (filterValue == "hoat-hinh") {
            final genreId = _genresMap["hoat-hinh"] ?? "10";
            endpoint = "/content_by_genre_id?id=$genreId&page=$page";
        }
    } else if (filterType == "the-loai") {
        final genreId = _genresMap[filterValue];
        if (genreId != null) {
            endpoint = "/content_by_genre_id?id=$genreId&page=$page";
        } else {
            return {"status": true, "items": [], "paginate": {"current_page": page, "total_page": 0}};
        }
    } else if (filterType == "quoc-gia") {
        final countryId = _countriesMap[filterValue];
        if (countryId != null) {
            endpoint = "/content_by_country_id?id=$countryId&page=$page";
        } else {
            return {"status": true, "items": [], "paginate": {"current_page": page, "total_page": 0}};
        }
    }
    
    final data = await _fetchWithFallback(endpoint);
    List<dynamic> movies = [];
    if (data is List) {
        movies = data;
    } else if (data is Map) {
        movies = data['movies'] ?? data['tvseries'] ?? data['content'] ?? [];
    }
    
    final mappedItems = movies.map((m) {
        final apiType = m['is_tvseries'] == "1" ? "series" : "movie";
        final String title = (m['title'] ?? '').toString();
        final cleanTitle = title.replaceAll(RegExp(r'\s*\(\d{4}\).*$'), '').trim();
        final engMatch = RegExp(r'\(\d{4}\)\s*(.*)$').firstMatch(title);
        final origName = engMatch != null ? engMatch.group(1)!.trim() : cleanTitle;
        
        return {
            "_id": m['videos_id'],
            "name": cleanTitle,
            "slug": _makeSlug(cleanTitle),
            "original_name": origName,
            "origin_name": origName,
            "poster_url": m['poster_url'] ?? m['thumbnail_url'],
            "thumb_url": m['thumbnail_url'] ?? m['poster_url'],
            "year": m['release'] ?? "",
            "quality": (m['video_quality'] ?? "").toString().contains("TM") ? "Premium TM" : "Premium",
            "current_episode": m['is_tvseries'] == "1" ? "Series" : "Full",
            "time": m['runtime'] ?? "N/A",
            "language": "Vietsub",
            "description": m['description'] ?? "",
            "type": apiType,
            "raw_payload": m['videos_id']
        };
    }).toList();
    
    return {
        "status": true,
        "items": mappedItems,
        "paginate": {"current_page": page, "total_page": 10}
    };
  }

  static Future<Map<String, dynamic>> searchMovies(String keyword) async {
    await _fetchMetadata();
    final encodedKw = Uri.encodeComponent(keyword);
    List<dynamic> movies = [];
    try {
      final res1 = _fetchWithFallback("/search?q=$encodedKw&type=movie");
      final res2 = _fetchWithFallback("/search?q=$encodedKw&type=tvseries");
      final results = await Future.wait([res1, res2]);
      
      final mData = results[0];
      final tData = results[1];
      if (mData is Map && mData['movie'] is List) movies.addAll(mData['movie']);
      if (tData is Map && tData['tvseries'] is List) movies.addAll(tData['tvseries']);
    } catch (e) {
       print('[PremiumApi] searchMovies failed: $e');
    }
    
    return {
      "status": true,
      "items": movies,
      "paginate": {"current_page": 1, "total_page": 10}
    };
  }

  static Future<Map<String, dynamic>> getDetail(String fullSlug) async {
    await _fetchMetadata();
    String apiType = "";
    String id = "";
    
    if (!fullSlug.startsWith("premium-")) {
       final keyword = fullSlug.replaceAll('-', ' ');
       final searchRes = await searchMovies(keyword);
       final items = searchRes['items'] as List;
       
       dynamic matched;
       for (var i in items) {
         final String title = (i['title'] ?? '').toString();
         final cleanTitle = title.replaceAll(RegExp(r'\s*\(\d{4}\).*$'), '').trim();
         final engMatch = RegExp(r'\(\d{4}\)\s*(.*)$').firstMatch(title);
         final origName = engMatch != null ? engMatch.group(1)!.trim() : cleanTitle;
         
         if (_makeSlug(cleanTitle) == fullSlug || _makeSlug(origName) == fullSlug) {
             matched = i;
             break;
         }
       }
       
       if (matched != null) {
          apiType = matched['is_tvseries'] == "1" ? "tvseries" : "movie";
          id = matched['videos_id'].toString();
       } else {
          throw Exception("Not found in premium");
       }
    } else {
       final parts = fullSlug.split('-');
       if (parts.length < 3) throw Exception("Invalid premium slug");
       apiType = parts[1] == "series" ? "tvseries" : "movie";
       id = parts.sublist(2).join('-');
    }
    
    final endpoint = "/single_details?type=$apiType&id=$id";
    final data = await _fetchWithFallback(endpoint);
    if (data == null) throw Exception("No detail data");
    
    List<Map<String, dynamic>> resolvedEpisodes = [];
    
    if (apiType == "movie") {
      final videos = data['videos'] as List? ?? [];
      List<Map<String, dynamic>> items = [];
      for (int idx = 0; idx < videos.length; idx++) {
         final v = videos[idx];
         final rawId = v['file_url']?.toString().split('/').last ?? '';
         if (rawId.isEmpty) continue;
         
         final rawLabel = v['label']?.toString() ?? '';
         final resMatch = RegExp(r'(1080p|2160p|720p|4k)', caseSensitive: false).firstMatch(rawLabel);
         final resolution = resMatch != null ? resMatch.group(1)!.toUpperCase() : '';
         final sizeMatch = RegExp(r'([\d\.]+\s*(GB|MB))', caseSensitive: false).firstMatch(rawLabel);
         final size = sizeMatch != null ? sizeMatch.group(1)! : '';
         
         String epName = "Full";
         if (resolution.isNotEmpty || size.isNotEmpty) {
            epName = [resolution, size].where((e) => e.isNotEmpty).join(' - ');
         }
         
         items.add({
            "name": epName,
            "slug": "full-$idx",
            "filename": rawLabel.isNotEmpty ? rawLabel : epName,
            "link": "premium://play/$rawId",
            "link_m3u8": "premium://play/$rawId",
            "isTM": RegExp(r'\.VIE\.|[\.\-_]TM[\.\-_]|Thuyet Minh|Long Tieng', caseSensitive: false).hasMatch(rawLabel)
         });
      }
      
      final hasTM = items.any((i) => i['isTM'] == true);
      resolvedEpisodes.add({
         "server_name": hasTM ? "Premium TM" : "Premium",
         "server_data": items
      });
    } else {
      final seasons = data['season'] as List? ?? [];
      for (var season in seasons) {
         final eps = season['episodes'] as List? ?? [];
         List<Map<String, dynamic>> items = [];
         for (var ep in eps) {
            final rawId = ep['file_url']?.toString().split('/').last ?? '';
            if (rawId.isEmpty) continue;
            
            final rawLabel = ep['episodes_name']?.toString() ?? '';
            String cleanName = rawLabel;
            final match = RegExp(r'S\d+E(\d+)|E(\d+)', caseSensitive: false).firstMatch(cleanName);
            if (match != null) {
                cleanName = int.parse(match.group(1) ?? match.group(2) ?? '0').toString();
            } else if (cleanName.contains('.')) {
                cleanName = cleanName.split('.')[0];
            }
            if (cleanName.toLowerCase() == 'full') cleanName = 'Full';
            
            String epName = (cleanName.toLowerCase() == 'full' || cleanName.toLowerCase() == 'hd' || cleanName.toLowerCase().contains('cam')) 
                ? cleanName 
                : "Tập $cleanName";
                
            final resMatch = RegExp(r'(1080p|2160p|720p|4k)', caseSensitive: false).firstMatch(rawLabel);
            final resolution = resMatch != null ? resMatch.group(1)!.toUpperCase() : '';
            final sizeMatch = RegExp(r'([\d\.]+\s*(GB|MB))', caseSensitive: false).firstMatch(rawLabel);
            final size = sizeMatch != null ? sizeMatch.group(1)! : '';
            
            if (resolution.isNotEmpty || size.isNotEmpty) {
                epName = "$epName (" + [resolution, size].where((e) => e.isNotEmpty).join(' - ') + ")";
            }
            
            items.add({
                "name": epName,
                "slug": "tap-" + _makeSlug(cleanName),
                "filename": rawLabel.isNotEmpty ? rawLabel : epName,
                "link": "premium://play/$rawId",
                "link_m3u8": "premium://play/$rawId",
                "isTM": RegExp(r'\.VIE\.|[\.\-_]TM[\.\-_]|Thuyet Minh|Long Tieng', caseSensitive: false).hasMatch(rawLabel)
            });
         }
         final hasTM = items.any((i) => i['isTM'] == true);
         final sn = season['seasons_name']?.toString() ?? "Season";
         if (items.isNotEmpty) {
           resolvedEpisodes.add({
              "server_name": hasTM ? "Premium TM - $sn" : "Premium - $sn",
              "server_data": items
           });
         }
      }
    }
    
    return {
      "status": true,
      "movie": {
         "_id": data['videos_id'],
         "name": data['title'],
         "slug": fullSlug,
         "origin_name": data['title'],
         "content": data['description'] ?? "",
         "type": apiType == "tvseries" ? "series" : "single",
         "status": "completed",
         "thumb_url": data['thumbnail_url'],
         "poster_url": data['poster_url'],
         "time": data['runtime'],
         "episode_current": data['is_tvseries'] == "1" ? "Series" : "Full",
         "quality": "Premium",
         "lang": "Vietsub",
         "year": data['release'],
         "casts": data['cast'] != null ? (data['cast'] as List).map((c) => c['name']).join(", ") : "",
         "director": data['director'] != null ? (data['director'] as List).map((d) => d['name']).join(", ") : "",
         "category": data['genre'] != null ? (data['genre'] as List).map((g) => {"name": g['name']}).toList() : [],
         "cast_and_crew": data['cast_and_crew'] ?? [],
         "episodes": resolvedEpisodes
      }
    };
  }
}
