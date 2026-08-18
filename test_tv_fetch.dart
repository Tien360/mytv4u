import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;

class TvChannel {
  final String id;
  final String name;
  final String category;
  final String streamUrl;
  final String webUrl;

  TvChannel({required this.id, required this.name, required this.category, required this.streamUrl, required this.webUrl});
}

void main() async {
  List<TvChannel> channels = [];
  try {
    final response = await http.get(Uri.parse('https://tinhlagi.pro/tivi/'));
    if (response.statusCode == 200) {
      final document = html_parser.parse(response.body);
      final headings = document.querySelectorAll('h2.group-title');
      
      for (var heading in headings) {
        String category = heading.text.trim();
        category = category.replaceAll(RegExp(r'\s*\(\d+\)$'), '').trim();
        
        final grid = heading.nextElementSibling;
        if (grid != null && grid.classes.contains('channel-grid')) {
          final aTags = grid.querySelectorAll('a.channel-card');
          
          for (var a in aTags) {
            final href = a.attributes['href'] ?? '';
            final uri = Uri.parse('https://tinhlagi.pro/tivi/' + href);
            String streamUrl = uri.queryParameters['url'] ?? '';
            final name = uri.queryParameters['name'] ?? a.querySelector('.channel-name')?.text.trim() ?? 'Unknown';
            final logo = a.querySelector('img')?.attributes['src'] ?? '';
            
            if (streamUrl.contains('youtube.com') || streamUrl.contains('youtu.be')) continue;
            
            String webUrl = '';
            if (streamUrl.contains('.mpd')) {
              webUrl = uri.toString();
              streamUrl = '';
            }
            
            String mappedCategory = category;
            
            if ((streamUrl.isNotEmpty || webUrl.isNotEmpty) && !channels.any((c) => (streamUrl.isNotEmpty && c.streamUrl == streamUrl) || c.name == name)) {
              channels.add(TvChannel(
                id: 'tl_$name',
                name: name,
                category: mappedCategory,
                streamUrl: streamUrl,
                webUrl: webUrl,
              ));
            } else {
              print('Skipped: $name, streamUrl: $streamUrl, webUrl: $webUrl');
            }
          }
        }
      }
    } else {
      print('Status: ${response.statusCode}');
    }
  } catch (e) {
    print('Error: $e');
  }
  print('Total added: ${channels.length}');
}
