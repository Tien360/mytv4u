import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final url = 'https://phim.nguonc.com/api/films/tim-kiem?keyword=thu+ky+kim+sao+the&limit=1';
  final res = await http.get(Uri.parse(url));
  final data = json.decode(res.body);
  print('nguonc type: ${data['items'][0]['type'] ?? data['items'][0]['type_name'] ?? 'none'}');
}
