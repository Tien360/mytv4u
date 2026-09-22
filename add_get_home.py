import re

with open("lib/api/premium_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

get_home_list = """
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
"""

content = content.replace("  static Future<Map<String, dynamic>> searchMovies(String keyword) async {", get_home_list + "\n  static Future<Map<String, dynamic>> searchMovies(String keyword) async {")

with open("lib/api/premium_api.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Added getHomeList")
