import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;

void main() async {
  final url = 'https://motchillv.io';
  print('Fetching: $url');
  final res = await http.get(Uri.parse(url));
  print('Status: ${res.statusCode}');
  
  if (res.statusCode == 200) {
    final doc = html_parser.parse(res.body);
    final items = doc.querySelectorAll('.item, .mtc-card'); // whatever class motchill uses
    if (items.isEmpty) {
        print('No items found using .item or .mtc-card. Let us just print all imgs.');
        final imgs = doc.querySelectorAll('img');
        for (var i = 0; i < (imgs.length > 5 ? 5 : imgs.length); i++) {
            print(imgs[i].outerHtml);
        }
    } else {
        print('Items found: ${items.length}');
        for (var i = 0; i < (items.length > 5 ? 5 : items.length); i++) {
            final img = items[i].querySelector('img');
            print(img?.outerHtml);
        }
    }
  }
}
