import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;
void main() async {
  final res = await http.get(Uri.parse('https://stream-proxy.oxaliplatin.workers.dev/?url=https%3A%2F%2Fmotchillv.co%2Fphim%2Ftho-san-quai-vat-dong-mau-khoi-nguon%2Ftap-1'));
  final doc = html_parser.parse(res.body);
  final buttons = doc.querySelectorAll('.streaming-server, [data-link]');
  for (var btn in buttons) {
    print('text: ${btn.text.trim()}, data-link: ${btn.attributes['data-link']}');
  }
}
