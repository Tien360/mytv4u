import 'package:http/http.dart' as http;

void main() async {
  final url = Uri.parse('https://tinhlagi.pro/sport/proxy.php?hash=bcb202d1e979241a1ff92374dae6f4f677e02ed970f92f1cc67d730f0641232c&referer=https%3A%2F%2Flive.chuoichien.tv%2F&url=https%3A%2F%2Fstm9ee346727718.stream.hdplaylink.com%2Fcctvlive%2Fchuoinhohd%2Fplaylist.m3u8');
  
  final client = http.Client();
  try {
    final request = http.Request('GET', url);
    final response = await client.send(request);
    
    print('Status: ${response.statusCode}');
    print('Headers: ${response.headers}');
    print('Location: ${response.headers['location']}');
    
    final body = await response.stream.bytesToString();
    print('Body length: ${body.length}');
    if (body.length < 500) {
      print('Body: $body');
    }
  } finally {
    client.close();
  }
}
