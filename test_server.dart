import 'dart:io';

void main() async {
  var server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
  print('Port: ${server.port}');
  
  server.listen((HttpRequest request) {
    print('request.uri.toString(): ${request.uri.toString()}');
    print('request.requestedUri.toString(): ${request.requestedUri.toString()}');
    request.response.close();
    server.close();
  });
  
  await HttpClient().getUrl(Uri.parse('http://localhost:${server.port}/tiktok/foo?bar=1&x=2')).then((req) => req.close());
}
