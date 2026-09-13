
import 'dart:convert';
import 'dart:io';

void main() async {
  final urls = [
    'https://phimapi.com/v1/api/tim-kiem?keyword=Silo'
  ];
  final file = File('test_meta.txt');
  final sink = file.openWrite();
  for (var url in urls) {
    try {
      final client = HttpClient();
      final req = await client.getUrl(Uri.parse(url));
      final res = await req.close();
      final str = await res.transform(utf8.decoder).join();
      sink.writeln(str);
    } catch(e) {}
  }
  await sink.close();
}

