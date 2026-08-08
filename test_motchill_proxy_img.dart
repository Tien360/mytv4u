import 'package:http/http.dart' as http;

void main() async {
  final imgUrl = 'https://motchillv.io/storage/hinh-anh/ve-nen-giac-mo-ngay-cuoi-poster.jpg';
  final url = 'https://stream-proxy.oxaliplatin.workers.dev/?url=${Uri.encodeComponent(imgUrl)}';
  print('Fetching: $url');
  final res = await http.get(Uri.parse(url));
  print('Status: ${res.statusCode}');
  print('Content-Type: ${res.headers['content-type']}');
  if (res.statusCode == 200) {
      print('Image size: ${res.bodyBytes.length}');
  }
}
