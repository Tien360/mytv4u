import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;

void main() async {
  final response = await http.get(Uri.parse('https://tinhlagi.pro/tivi/'));
  final document = html_parser.parse(response.body);
  
  int totalChannels = 0;
  final headings = document.querySelectorAll('h2.group-title');
  for (var heading in headings) {
    String category = heading.text.trim();
    category = category.replaceAll(RegExp(r'\s*\(\d+\)$'), '').trim();
    
    final grid = heading.nextElementSibling;
    if (grid != null && grid.classes.contains('channel-grid')) {
      final aTags = grid.querySelectorAll('a.channel-card');
      print('Category: $category, found ${aTags.length} channels');
      totalChannels += aTags.length;
      
      for (var a in aTags) {
        final href = a.attributes['href'] ?? '';
        final uri = Uri.parse('https://tinhlagi.pro/tivi/' + href);
        final streamUrl = uri.queryParameters['url'] ?? '';
        final name = uri.queryParameters['name'] ?? a.querySelector('.channel-name')?.text.trim() ?? 'Unknown';
        
        if (streamUrl.contains('.mpd')) {
          print('FOUND MPD: $streamUrl');
        }
      }
    }
  }
  print('Total channels matched: $totalChannels');
}
