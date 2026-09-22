import 'package:http/http.dart' as http;

void main() async {
  try {
    final client = http.Client();
    final request = http.Request('GET', Uri.parse('https://rip.cryboiz.workers.dev/go/free1'))
      ..followRedirects = false;
    final response = await client.send(request).timeout(const Duration(seconds: 5));
    
    String? location;
    if (response.statusCode == 301 || response.statusCode == 302 || response.statusCode == 307 || response.statusCode == 308) {
       location = response.headers['location'];
    }
    if (location != null && location.isNotEmpty) {
       if (location.endsWith('/')) {
           location = location.substring(0, location.length - 1);
       }
       print('URL: ' + location);
       print('List: ' + location + '/danh-sach');
    }
  } catch (e) {
    print(e);
  }
}
