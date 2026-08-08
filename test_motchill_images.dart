import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;

void main() async {
  final baseUrl = 'https://motchillv.io/danh-sach/phim-moi';
  final url = 'https://stream-proxy.oxaliplatin.workers.dev/?url=${Uri.encodeComponent(baseUrl)}';
  print('Fetching: $url');
  final res = await http.get(Uri.parse(url));
  print('Status: ${res.statusCode}');
  
  if (res.statusCode == 200) {
    final doc = html_parser.parse(res.body);
    final aTags = doc.querySelectorAll('a[href*="/phim/"]');
    print('Found ${aTags.length} links with /phim/');
    int printed = 0;
    for (int i = 0; i < aTags.length; i++) {
        final img = aTags[i].querySelector('img');
        if (img != null) {
            print(aTags[i].outerHtml);
            printed++;
            if (printed >= 5) break;
        }
    }
  }
}
