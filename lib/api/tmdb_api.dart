import 'dart:convert';
import 'package:http/http.dart' as http;

class TmdbApi {
  static const String _apiKey = 'e9e9d8da18ae29fc430845952232787c';
  static const String _baseUrl = 'https://api.themoviedb.org/3';
  static const String _imageBaseUrl = 'https://image.tmdb.org/t/p/w500';

  /// Lấy hình ảnh TMDB đầy đủ
  static String getImageUrl(String? path) {
    if (path == null || path.isEmpty) return '';
    return '$_imageBaseUrl$path';
  }

  /// Tìm TMDB ID dựa trên IMDB ID hoặc Tên phim
  static Future<int?> getTmdbTvId({String? imdbId, required String originalName, String? year}) async {
    try {
      // 1. Thử tìm bằng IMDB ID trước
      if (imdbId != null && imdbId.isNotEmpty) {
        final findUrl = '$_baseUrl/find/$imdbId?api_key=$_apiKey&external_source=imdb_id';
        final res = await http.get(Uri.parse(findUrl)).timeout(const Duration(seconds: 10));
        if (res.statusCode == 200) {
          final data = json.decode(utf8.decode(res.bodyBytes));
          final tvResults = data['tv_results'] as List?;
          if (tvResults != null && tvResults.isNotEmpty) {
            return tvResults[0]['id'] as int;
          }
        }
      }

      // 2. Nếu không có hoặc không tìm thấy bằng IMDB ID, tìm bằng Tên
      if (originalName.isNotEmpty) {
        String searchUrl = '$_baseUrl/search/tv?api_key=$_apiKey&query=${Uri.encodeComponent(originalName)}';
        if (year != null && year.isNotEmpty && year != '0') {
           // Năm phim từ API KKPhim đôi khi có dạng 2023-2024, lấy phần đầu
           final y = year.split('-')[0].trim();
           searchUrl += '&first_air_date_year=$y';
        }
        final res = await http.get(Uri.parse(searchUrl)).timeout(const Duration(seconds: 10));
        if (res.statusCode == 200) {
          final data = json.decode(utf8.decode(res.bodyBytes));
          final results = data['results'] as List?;
          if (results != null && results.isNotEmpty) {
            return results[0]['id'] as int;
          }
        }
      }
    } catch (e) {
      print('Lỗi lấy TMDB ID: $e');
    }
    return null;
  }

  /// Lấy thông tin chi tiết Phim bộ (để biết có bao nhiêu season)
  static Future<Map<String, dynamic>?> getTvDetails(int tmdbId, String language) async {
    try {
      final lang = language == 'vi' ? 'vi-VN' : 'en-US';
      final url = '$_baseUrl/tv/$tmdbId?api_key=$_apiKey&language=$lang';
      final res = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 10));
      if (res.statusCode == 200) {
        return json.decode(utf8.decode(res.bodyBytes));
      }
    } catch (e) {
      print('Lỗi lấy TvDetails: $e');
    }
    return null;
  }

  /// Lấy danh sách các tập của một Season
  static Future<List<dynamic>> getSeasonEpisodes(int tmdbId, int seasonNumber, String language) async {
    try {
      final lang = language == 'vi' ? 'vi-VN' : 'en-US';
      final url = '$_baseUrl/tv/$tmdbId/season/$seasonNumber?api_key=$_apiKey&language=$lang';
      final res = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 10));
      if (res.statusCode == 200) {
        final data = json.decode(utf8.decode(res.bodyBytes));
        final episodes = data['episodes'] as List<dynamic>? ?? [];
        
        if (language == 'vi') {
          bool needsEnglish = episodes.any((ep) => (ep['overview'] == null || ep['overview'].isEmpty) || (ep['name'] == null || ep['name'].isEmpty));
          
          if (needsEnglish) {
            final urlEn = '$_baseUrl/tv/$tmdbId/season/$seasonNumber?api_key=$_apiKey&language=en-US';
            final resEn = await http.get(Uri.parse(urlEn)).timeout(const Duration(seconds: 10));
            if (resEn.statusCode == 200) {
              final dataEn = json.decode(utf8.decode(resEn.bodyBytes));
              final episodesEn = dataEn['episodes'] as List<dynamic>? ?? [];
              
              for (int i = 0; i < episodes.length; i++) {
                if (i < episodesEn.length) {
                  final epVi = episodes[i];
                  final epEn = episodesEn[i];
                  if (epVi['overview'] == null || epVi['overview'].isEmpty) {
                    if (epEn['overview'] != null && epEn['overview'].isNotEmpty) {
                      epVi['overview'] = epEn['overview'];
                      epVi['_needs_translation'] = true;
                    }
                  }
                  if (epVi['name'] == null || epVi['name'].isEmpty) {
                    if (epEn['name'] != null && epEn['name'].isNotEmpty) {
                      epVi['name'] = epEn['name'];
                    }
                  }
                }
              }
            }
          }
        }
        
        return episodes;
      }
    } catch (e) {
      print('Lỗi lấy SeasonEpisodes: $e');
    }
    return [];
  }
}
