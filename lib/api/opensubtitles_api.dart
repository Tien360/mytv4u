import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:media_kit/media_kit.dart';

class OpenSubtitlesApi {
  static const String _baseUrl = 'https://opensubtitles-v3.strem.io';

  /// Fetch subtitles from OpenSubtitles v3 addon
  /// Returns a list of SubtitleTrack objects ready to be used by media_kit
  static Future<List<SubtitleTrack>> fetchSubtitles(String imdbId, {int? season, int? episode}) async {
    try {
      String type;
      String id;
      if (season != null && episode != null) {
        type = 'series';
        id = '$imdbId:$season:$episode';
      } else {
        type = 'movie';
        id = imdbId;
      }

      final url = '$_baseUrl/subtitles/$type/$id.json';
      print('OpenSubtitlesApi: Fetching from $url');
      
      final res = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 10));
      if (res.statusCode != 200) {
        print('OpenSubtitlesApi: HTTP ${res.statusCode}');
        return [];
      }

      final data = json.decode(res.body);
      final subtitles = data['subtitles'] as List<dynamic>?;
      if (subtitles == null || subtitles.isEmpty) return [];

      final List<SubtitleTrack> tracks = [];
      
      // Keep track of counts to name them uniquely
      int vieCount = 1;
      int engCount = 1;

      for (var sub in subtitles) {
        if (sub is! Map<String, dynamic>) continue;
        
        final lang = sub['lang'] as String?;
        final url = sub['url'] as String?;
        if (url == null || url.isEmpty) continue;

        if (lang == 'vie') {
          tracks.add(SubtitleTrack.uri(url, title: '[OpenSub] Tiếng Việt $vieCount', language: 'vie'));
          vieCount++;
        } else if (lang == 'eng') {
          tracks.add(SubtitleTrack.uri(url, title: '[OpenSub] English $engCount', language: 'eng'));
          engCount++;
        }
      }

      return tracks;
    } catch (e) {
      print('OpenSubtitlesApi error: $e');
      return [];
    }
  }
}
