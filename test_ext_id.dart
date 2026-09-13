import 'dart:convert';
import 'package:http/http.dart' as http;
void main() async {
  final url = 'https://api.themoviedb.org/3/tv/125988?api_key=e9e9d8da18ae29fc430845952232787c&append_to_response=external_ids';
  final res = await http.get(Uri.parse(url));
  print(res.statusCode);
  if (res.statusCode == 200) {
    print(json.decode(res.body)['external_ids']);
  }
}
