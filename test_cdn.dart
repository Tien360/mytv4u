import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  try {
    final client = http.Client();
    final request = http.Request('GET', Uri.parse('https://rip.cryboiz.workers.dev/go/cdn'))
      ..followRedirects = false;
    final response = await client.send(request);
    print("Status: ${response.statusCode}");
    print("Headers: ${response.headers}");
    final body = await response.stream.bytesToString();
    print("Body: $body");
  } catch (e) {
    print("Error: $e");
  }
}
