import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;

void main() async {
  final baseUrl = 'https://motchillv.io';
  final url = 'https://stream-proxy.oxaliplatin.workers.dev/?url=${Uri.encodeComponent(baseUrl)}';
  final res = await http.get(Uri.parse(url));
  
  if (res.statusCode == 200) {
    final doc = html_parser.parse(res.body);
    final imgs = doc.querySelectorAll('img');
    int printed = 0;
    for (int i = 20; i < imgs.length; i++) {
      final img = imgs[i];
      final parent = img.parent;
      if (parent != null && parent.localName == 'a' && parent.attributes['href'] != null && parent.attributes['href']!.contains('/phim/')) {
        print('--- img class: ${img.className} ---');
        print(parent.outerHtml);
        printed++;
        if (printed >= 5) break;
      }
    }
  }
}
