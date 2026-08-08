import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents:runQuery');
  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'structuredQuery': {
        'from': [{'collectionId': 'comments'}],
        'where': {
          'fieldFilter': {
            'field': {'fieldPath': 'movieSlug'},
            'op': 'EQUAL',
            'value': {'stringValue': 'full'} // replacing with a valid slug if needed
          }
        }
      }
    }),
  );
  print(response.statusCode);
  print(response.body);
}
