import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;

void main() async {
  final baseUrl = 'https://motchillv.io';
  final url = 'https://stream-proxy.oxaliplatin.workers.dev/?url=${Uri.encodeComponent(baseUrl)}';
  print('Fetching: $url');
  final res = await http.get(Uri.parse(url));
  print('Status: ${res.statusCode}');
  
  if (res.statusCode == 200) {
    final doc = html_parser.parse(res.body);
    final items = doc.querySelectorAll('.item, .mtc-card');
    if (items.isEmpty) {
        print('No items found using .item or .mtc-card.');
        final imgs = doc.querySelectorAll('img');
        for (var i = 0; i < (imgs.length > 5 ? 5 : imgs.length); i++) {
            print(imgs[i].outerHtml);
        }
    } else {
        print('Items found: ${items.length}');
        for (var i = 0; i < (items.length > 5 ? 5 : items.length); i++) {
            print(items[i].outerHtml);
        }
    }
  } else {
    print(res.body);
  }
}
