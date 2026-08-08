import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/comments');
  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'fields': {
        'movieSlug': {'stringValue': 'test-movie-slug'},
        'userId': {'stringValue': 'test-uid'},
        'userDisplayName': {'stringValue': 'Test User'},
        'userPhoto': {'stringValue': 'https://via.placeholder.com/150'},
        'text': {'stringValue': 'This is a test comment from Flutter REST'},
        'timestamp': {'timestampValue': DateTime.now().toUtc().toIso8601String()},
        'replies': {'arrayValue': {'values': []}}
      }
    }),
  );
  print(response.statusCode);
  print(response.body);
}
