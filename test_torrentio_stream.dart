import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final url = 'https://torrentio.strem.fun/stream/series/tt8242904:1:3.json';
  print('Fetching: $url');
  final res = await http.get(Uri.parse(url));
  print('Status: ${res.statusCode}');
  if (res.statusCode == 200) {
    final data = json.decode(res.body);
    final streams = data['streams'] as List?;
    print('Streams: ${streams?.length}');
    if (streams != null && streams.isNotEmpty) {
      print(streams.first);
    }
  }
}
