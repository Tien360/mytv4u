import 'package:http/http.dart' as http;
void main() async {
  final url = 'https://stream-proxy.oxaliplatin.workers.dev/?url=' + Uri.encodeComponent('https://motchillv.io/xem-phim/tho-san-quai-vat-phan-1-tap-1');
  final res = await http.get(Uri.parse(url));
  print(res.statusCode);
  print(res.body.substring(0, 50));
}
