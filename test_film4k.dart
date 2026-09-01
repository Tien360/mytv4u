import 'package:http/http.dart' as http;

void main() async {
  final url = Uri.parse('https://film4k.net/api');
  try {
    final response = await http.get(url, headers: {'User-Agent': 'Mozilla/5.0'});
    print(response.statusCode);
  } catch (e) {
    print(e);
  }
}
