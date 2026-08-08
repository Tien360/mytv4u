import 'package:http/http.dart' as http;
void main() async {
  final res = await http.get(Uri.parse('https://motchillv.io'));
  print(res.statusCode);
}
