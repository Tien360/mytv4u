import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;

void main() async {
  final baseUrl = 'https://motchillv.io/danh-sach/phim-moi';
  final url = 'https://stream-proxy.oxaliplatin.workers.dev/?url=${Uri.encodeComponent(baseUrl)}';
  final res = await http.get(Uri.parse(url));
  
  if (res.statusCode == 200) {
    final doc = html_parser.parse(res.body);
    final aTags = doc.querySelectorAll('a[href*="/phim/"]');
    final titles = <String>[];
    for (int i = 0; i < aTags.length; i++) {
        final img = aTags[i].querySelector('img');
        if (img != null) {
            final title = aTags[i].attributes['title'];
            if (title != null) titles.add(title);
        }
    }
    print('Total movies: ${titles.length}');
    print('Unique movies: ${titles.toSet().length}');
    
    // find duplicates
    final seen = <String>{};
    for (final title in titles) {
        if (seen.contains(title)) {
            print('Duplicate found: $title');
        }
        seen.add(title);
    }
  }
}
