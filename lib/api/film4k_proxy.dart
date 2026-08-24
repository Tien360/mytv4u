import 'dart:io';
import 'dart:async';
import 'package:http/http.dart' as http;

class Film4kProxy {
  static HttpServer? _server;
  static int _port = 0;

  static Future<void> start() async {
    if (_server != null) return;
    
    _server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
    _port = _server!.port;
    print('Film4kProxy started on port $_port');

    _server!.listen((HttpRequest request) async {
      final path = request.uri.path;
      
      if (path.startsWith('/api/hls/')) {
        final url = 'https://film4k.net${request.uri.toString()}';
        try {
          final response = await http.get(Uri.parse(url), headers: {'User-Agent': 'Mozilla/5.0'});
          
          if (response.statusCode == 200) {
            String content = response.body;
            content = content.replaceAllMapped(RegExp(r'https://[^"\n\r]+'), (match) {
              final original = match.group(0)!;
              if (original.contains('tiktokcdn.com')) {
                return 'http://localhost:$_port/chunk?url=${Uri.encodeComponent(original)}';
              }
              return original;
            });
            content = content.replaceAll('https://film4k.net/api/hls/', 'http://localhost:$_port/api/hls/');
            
            request.response.statusCode = 200;
            request.response.headers.add('Access-Control-Allow-Origin', '*');
            request.response.headers.contentType = ContentType.parse('application/vnd.apple.mpegurl');
            request.response.write(content);
            await request.response.close();
          } else {
            request.response.statusCode = response.statusCode;
            await request.response.close();
          }
        } catch (e) {
          request.response.statusCode = 500;
          await request.response.close();
        }
      } else if (path.startsWith('/chunk')) {
        final realUrl = request.uri.queryParameters['url'];
        if (realUrl == null || realUrl.isEmpty) {
          request.response.statusCode = 400;
          await request.response.close();
          return;
        }
        
        try {
          final client = http.Client();
          final requestHttp = http.Request('GET', Uri.parse(realUrl));
          requestHttp.headers['User-Agent'] = 'Mozilla/5.0';
          
          final streamedResponse = await client.send(requestHttp);
          
          if (streamedResponse.statusCode == 200 || streamedResponse.statusCode == 206) {
            request.response.statusCode = 200;
            request.response.headers.add('Access-Control-Allow-Origin', '*');
            // Allow media_kit to infer from the stream or URL
            request.response.headers.contentType = ContentType.parse('application/octet-stream');
            
            List<int> buffer = [];
            bool headerSkipped = false;
            final iend = [73, 69, 78, 68, 174, 66, 96, 130];
            bool isPngStego = true;
            
            StreamSubscription? sub;
            
            request.response.done.then((_) {
              sub?.cancel();
              client.close();
            }).catchError((_) {
              sub?.cancel();
              client.close();
            });

            sub = streamedResponse.stream.listen((chunk) {
              if (headerSkipped) {
                try {
                  request.response.add(chunk);
                } catch (_) {
                  sub?.cancel();
                  client.close();
                }
              } else {
                buffer.addAll(chunk);
                
                if (isPngStego) {
                  int idx = -1;
                  for (int i = 0; i <= buffer.length - 8; i++) {
                    bool match = true;
                    for (int j = 0; j < 8; j++) {
                      if (buffer[i + j] != iend[j]) {
                        match = false;
                        break;
                      }
                    }
                    if (match) {
                      idx = i;
                      break;
                    }
                  }
                  
                  if (idx != -1) {
                    headerSkipped = true;
                    try {
                      request.response.add(buffer.sublist(idx + 8));
                    } catch (_) {
                      sub?.cancel();
                      client.close();
                    }
                    buffer.clear();
                  } else if (buffer.length > 50 * 1024) {
                    // If no PNG header found within first 50KB, it is a normal file!
                    isPngStego = false;
                    headerSkipped = true;
                    try {
                      request.response.add(buffer);
                    } catch (_) {
                      sub?.cancel();
                      client.close();
                    }
                    buffer.clear();
                  }
                }
              }
            }, onDone: () async {
              try {
                if (!headerSkipped && buffer.isNotEmpty) {
                  request.response.add(buffer);
                }
                await request.response.close();
              } catch (_) {}
              client.close();
            }, onError: (e) {
              try { request.response.close(); } catch (_) {}
              client.close();
            });
            
          } else {
            request.response.statusCode = streamedResponse.statusCode;
            await request.response.close();
            client.close();
          }
        } catch (e) {
          try {
            request.response.statusCode = 500;
            await request.response.close();
          } catch (_) {}
        }
      } else {
        request.response.statusCode = 404;
        await request.response.close();
      }
    });
  }

  static String processUrl(String originalUrl) {
    if (_port == 0 || originalUrl.isEmpty) return originalUrl;
    if (originalUrl.startsWith('https://film4k.net/api/hls/')) {
      return originalUrl.replaceFirst('https://film4k.net/api/hls/', 'http://localhost:$_port/api/hls/');
    }
    return originalUrl;
  }
}
