import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  const apiKey = 'e9e9d8da18ae29fc430845952232787c';
  final url = 'https://api.themoviedb.org/3/tv/94997/images?api_key=$apiKey';
  final res = await http.get(Uri.parse(url));
  final data = json.decode(res.body);
  print(data.keys);
  if (data['logos'] != null) {
      print('Logos count: ${data['logos'].length}');
      for (var logo in data['logos'].take(5)) {
          print('${logo['iso_639_1']} - ${logo['file_path']}');
      }
  }
}
