import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;
void main() async {
  final url = 'https://stream-proxy.oxaliplatin.workers.dev/?url=' + Uri.encodeComponent('https://motchillv.co/phim/venom-let-there-be-carnage/tap-full');
  final res = await http.get(Uri.parse(url));
  final doc = html_parser.parse(res.body);
  final buttons = doc.querySelectorAll('.streaming-server, [data-link], .server-item');
  for (var btn in buttons) {
    print('text: ${btn.text.trim()}, data-link: ${btn.attributes['data-link']}');
  }
}
