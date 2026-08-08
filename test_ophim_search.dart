import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  // Try ophim API
  final url = 'https://ophim1.com/v1/api/tim-kiem?keyword=thu+ky+kim+sao+the&limit=1';
  final res = await http.get(Uri.parse(url));
  final data = json.decode(res.body);
  print(data['data']['items'][0]);
}
