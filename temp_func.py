with open("lib/screens/movie_detail_screen_test.dart", "r", encoding="utf-8") as f:
    c = f.read()

import_line = "import '../utils/l10n.dart';"
c = c.replace(import_line, import_line + "\nimport '../utils/location_helper.dart';")

old_func = """  String? _getAgeRating() {
    if (_tmdbDetails == null) return null;
    
    // TV Shows
    if (_tmdbDetails!['content_ratings'] != null && _tmdbDetails!['content_ratings']['results'] != null) {
      final results = _tmdbDetails!['content_ratings']['results'] as List;
      var usRating = results.firstWhere((r) => r['iso_3166_1'] == 'US', orElse: () => null);
      if (usRating != null && usRating['rating'] != null && usRating['rating'].toString().isNotEmpty) {
        return usRating['rating'].toString();
      }
      for (var r in results) {
        if (r['rating'] != null && r['rating'].toString().isNotEmpty) return r['rating'].toString();
      }
    }
    
    // Movies
    if (_tmdbDetails!['release_dates'] != null && _tmdbDetails!['release_dates']['results'] != null) {
      final results = _tmdbDetails!['release_dates']['results'] as List;
      var usRating = results.firstWhere((r) => r['iso_3166_1'] == 'US', orElse: () => null);
      if (usRating != null && usRating['release_dates'] != null) {
        for (var d in usRating['release_dates']) {
          if (d['certification'] != null && d['certification'].toString().isNotEmpty) return d['certification'].toString();
        }
      }
      for (var r in results) {
        if (r['release_dates'] != null) {
          for (var d in r['release_dates']) {
             if (d['certification'] != null && d['certification'].toString().isNotEmpty) return d['certification'].toString();
          }
        }
      }
    }
    return null;
  }"""

new_func = """  String? _getAgeRating() {
    if (_tmdbDetails == null) return null;
    
    String userCountry = LocationHelper.userCountry;
    String? originCountry;
    if (_tmdbDetails!['origin_country'] != null && (_tmdbDetails!['origin_country'] as List).isNotEmpty) {
      originCountry = _tmdbDetails!['origin_country'][0].toString();
    }

    String? findRating(String countryCode) {
      // TV Shows
      if (_tmdbDetails!['content_ratings'] != null && _tmdbDetails!['content_ratings']['results'] != null) {
        final results = _tmdbDetails!['content_ratings']['results'] as List;
        var rMatch = results.firstWhere((r) => r['iso_3166_1'] == countryCode, orElse: () => null);
        if (rMatch != null && rMatch['rating'] != null && rMatch['rating'].toString().isNotEmpty) {
          return rMatch['rating'].toString();
        }
      }
      
      // Movies
      if (_tmdbDetails!['release_dates'] != null && _tmdbDetails!['release_dates']['results'] != null) {
        final results = _tmdbDetails!['release_dates']['results'] as List;
        var rMatch = results.firstWhere((r) => r['iso_3166_1'] == countryCode, orElse: () => null);
        if (rMatch != null && rMatch['release_dates'] != null) {
          for (var d in rMatch['release_dates']) {
            if (d['certification'] != null && d['certification'].toString().isNotEmpty) {
              return d['certification'].toString();
            }
          }
        }
      }
      return null;
    }

    // Ưu tiên 1: Quốc gia của người xem (theo IP)
    String? rating = findRating(userCountry);
    if (rating != null) return rating;

    // Ưu tiên 2: Quốc gia gốc của phim (Hàn Quốc, Nhật Bản...)
    if (originCountry != null) {
      rating = findRating(originCountry);
      if (rating != null) return rating;
    }

    // Ưu tiên 3: Fallback về Mỹ
    rating = findRating('US');
    if (rating != null) return rating;

    // Ưu tiên 4: Lấy bừa nhãn đầu tiên có thể tìm thấy nếu tất cả đều thất bại
    if (_tmdbDetails!['content_ratings'] != null && _tmdbDetails!['content_ratings']['results'] != null) {
        final results = _tmdbDetails!['content_ratings']['results'] as List;
        for (var r in results) {
          if (r['rating'] != null && r['rating'].toString().isNotEmpty) return r['rating'].toString();
        }
    }
    if (_tmdbDetails!['release_dates'] != null && _tmdbDetails!['release_dates']['results'] != null) {
        final results = _tmdbDetails!['release_dates']['results'] as List;
        for (var r in results) {
          if (r['release_dates'] != null) {
            for (var d in r['release_dates']) {
               if (d['certification'] != null && d['certification'].toString().isNotEmpty) return d['certification'].toString();
            }
          }
        }
    }
    
    return null;
  }"""

c = c.replace(old_func, new_func)

with open("lib/screens/movie_detail_screen_test.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated _getAgeRating!")
