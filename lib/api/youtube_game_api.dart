import 'dart:convert';
import 'package:http/http.dart' as http;

class YoutubeGameInfo {
  final String title;
  final String description;
  final String genre;
  final String developer;
  final String publisher;
  final String releaseDate;
  final String thumbUrl;

  YoutubeGameInfo({
    required this.title,
    required this.description,
    required this.genre,
    required this.developer,
    required this.publisher,
    required this.releaseDate,
    required this.thumbUrl,
  });
}

class YoutubeGameApi {
  static Future<YoutubeGameInfo?> fetchGameInfo(String url) async {
    try {
      final res = await http.get(Uri.parse(url), headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      });
      
      if (res.statusCode != 200) return null;
      
      final html = res.body;
      final RegExp ytDataRegex = RegExp(r'var ytInitialData = (\{.*?\});</script>');
      final match = ytDataRegex.firstMatch(html);
      
      if (match != null) {
        final data = json.decode(match.group(1)!);
        
        String title = '';
        String description = '';
        String genre = '';
        String developer = '';
        String publisher = '';
        String releaseDate = '';
        String thumbUrl = '';

        // Recursively find the game data
        void searchNode(dynamic node) {
          if (node is Map) {
            // Find title
            if (node.containsKey('title') && node['title'] is String) {
              if (title.isEmpty) title = node['title'];
            }
            // Find description
            if (node.containsKey('description') && node['description'] is String) {
              if (description.isEmpty) description = node['description'];
            }
            // Find genre
            if (node.containsKey('primaryGenre') && node['primaryGenre'] is String) {
              genre = node['primaryGenre'];
            }
            // Find infoRow
            if (node.containsKey('infoRow') && node['infoRow'] is List) {
              for (var row in node['infoRow']) {
                if (row['label'] == 'Nhà phát triển' || row['label'] == 'Developer') developer = row['value'] ?? '';
                if (row['label'] == 'Nhà xuất bản' || row['label'] == 'Publisher') publisher = row['value'] ?? '';
                if (row['label'] == 'Ngày phát hành' || row['label'] == 'Release date') releaseDate = row['value'] ?? '';
              }
            }
            // Find thumbnail
            if (node.containsKey('thumbnail') && node['thumbnail'] is Map && node['thumbnail'].containsKey('thumbnails')) {
              final thumbs = node['thumbnail']['thumbnails'] as List;
              if (thumbs.isNotEmpty) {
                // Get the highest resolution one
                thumbUrl = thumbs.last['url'] ?? '';
              }
            }
            
            node.forEach((key, value) {
              searchNode(value);
            });
          } else if (node is List) {
            for (var item in node) {
              searchNode(item);
            }
          }
        }
        
        searchNode(data);
        
        return YoutubeGameInfo(
          title: title,
          description: description,
          genre: genre,
          developer: developer,
          publisher: publisher,
          releaseDate: releaseDate,
          thumbUrl: thumbUrl,
        );
      }
    } catch (e) {
      print('Error fetching game info: $e');
    }
    return null;
  }
}
