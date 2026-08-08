import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final url = 'https://opensubtitles-v3.strem.io/subtitles/series/tt8242904:1:1.json';
  print('Fetching: $url');
  final res = await http.get(Uri.parse(url));
  print('Status: ${res.statusCode}');
  if (res.statusCode == 200) {
    final data = json.decode(res.body);
    final subs = data['subtitles'] as List?;
    print('Subs: ${subs?.length}');
    if (subs != null && subs.isNotEmpty) {
      print(subs.first);
    }
  }
}
