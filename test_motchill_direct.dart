import 'package:http/http.dart' as http;
void main() async {
  final res = await http.get(
    Uri.parse('https://motchillv.io'),
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    },
  );
  print(res.statusCode);
  print(res.body.substring(0, 100));
}
