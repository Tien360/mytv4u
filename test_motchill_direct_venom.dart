import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;
void main() async {
  final res = await http.get(
    Uri.parse('https://motchillv.co/phim/venom-let-there-be-carnage/tap-full'),
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    },
  );
  final doc = html_parser.parse(res.body);
  final buttons = doc.querySelectorAll('.streaming-server, [data-link], .server-item');
  for (var btn in buttons) {
    print('text: ${btn.text.trim()}, data-link: ${btn.attributes['data-link']}');
  }
}
