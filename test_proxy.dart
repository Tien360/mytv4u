import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'package:crypto/crypto.dart';
import 'package:encrypt/encrypt.dart' as encrypt;

class PremiumResolver {
  static Future<String?> getVideoStream(String fileId) async {
    const String secret2 = "5e8d1b4f9c2a6e730b1f8d4a92c5e3d1";
    final int nowSec = (DateTime.now().toUtc().millisecondsSinceEpoch / 1000).floor();
    final utcDt = DateTime.now().toUtc();
    final String dateStr = "${utcDt.year}${utcDt.month.toString().padLeft(2, '0')}${utcDt.day.toString().padLeft(2, '0')}";
    final keyBytes = sha256.convert(utf8.encode(secret2)).bytes;
    final ivFull = sha256.convert(utf8.encode('iv:' + secret2)).bytes;
    final ivBytes = Uint8List.fromList(ivFull.sublist(0, 12));
    final plaintext = utf8.encode("$secret2:$dateStr");
    final key = encrypt.Key(Uint8List.fromList(keyBytes));
    final iv = encrypt.IV(ivBytes);
    final encrypter = encrypt.Encrypter(encrypt.AES(key, mode: encrypt.AESMode.gcm));
    final encrypted = encrypter.encryptBytes(plaintext, iv: iv);
    final ciphertextHex = encrypted.bytes.map((b) => b.toRadixString(16).padLeft(2, '0')).join('');
    final signingSecret = "$secret2:$ciphertextHex";
    final hmacMask = Hmac(sha256, utf8.encode(signingSecret));
    final mask = hmacMask.convert(utf8.encode("otp-ts-mask")).bytes.sublist(0, 4);
    final tsBytes = Uint8List(4)..buffer.asByteData().setUint32(0, nowSec & 0xFFFFFFFF, Endian.big);
    final tsHexBytes = Uint8List(4);
    for (int i = 0; i < 4; i++) {
      tsHexBytes[i] = tsBytes[i] ^ mask[i];
    }
    final tsHex = tsHexBytes.map((b) => b.toRadixString(16).padLeft(2, '0')).join('');
    final hmacToken = Hmac(sha256, utf8.encode(signingSecret));
    final token = hmacToken.convert(utf8.encode("$fileId:$nowSec")).toString();
    final apiUrl = "https://sv1.p4k.dpdns.org/$fileId?token=$token&ts=$tsHex";
    try {
      final response = await http.get(Uri.parse(apiUrl), headers: {'User-Agent': 'okhttp/4.12.0'}).timeout(const Duration(seconds: 10));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['url']?.toString();
      }
    } catch (_) {}
    return null;
  }
}

class MultiThreadProxy {
  static HttpServer? _server;
  static const int chunkSize = 2 * 1024 * 1024; // 2MB
  static const int maxWorkers = 4;

  static Future<void> start() async {
    _server = await HttpServer.bind(InternetAddress.loopbackIPv4, 8081);
    print('[Proxy] Started on http://localhost:8081');

    _server!.listen((HttpRequest request) async {
      try {
        await _handleRequest(request);
      } catch (e) {
        try { request.response.statusCode = 500; await request.response.close(); } catch (_) {}
      }
    });
  }

  static Future<void> _handleRequest(HttpRequest request) async {
    final fileId = request.uri.queryParameters['id'];
    if (fileId == null) return;

    print('\n[Proxy] Đang lấy link thật cho ID: $fileId ...');
    final targetUrl = await PremiumResolver.getVideoStream(fileId);
    if (targetUrl == null) {
      print('[Proxy] Không lấy được link!');
      request.response.statusCode = 404;
      await request.response.close();
      return;
    }
    print('[Proxy] Link thật: $targetUrl');

    final client = http.Client();
    final headReq = http.Request('HEAD', Uri.parse(targetUrl));
    headReq.headers['User-Agent'] = 'okhttp/4.12.0';
    final headRes = await client.send(headReq);
    
    if (headRes.statusCode != 200 && headRes.statusCode != 206) {
      print('[Proxy] Lỗi HEAD, mã: ${headRes.statusCode}');
      request.response.statusCode = 500;
      await request.response.close();
      return;
    }

    final totalLength = int.tryParse(headRes.headers['content-length'] ?? '') ?? 0;
    int startByte = 0;
    int endByte = totalLength - 1;
    final rangeHeader = request.headers.value('range');
    
    if (rangeHeader != null && rangeHeader.startsWith('bytes=')) {
      final parts = rangeHeader.substring(6).split('-');
      startByte = int.tryParse(parts[0]) ?? 0;
      if (parts.length > 1 && parts[1].isNotEmpty) {
        endByte = int.tryParse(parts[1]) ?? (totalLength - 1);
      }
    }

    final contentLength = endByte - startByte + 1;
    
    request.response.statusCode = rangeHeader != null ? 206 : 200;
    request.response.headers.set('Content-Type', 'video/mp4');
    request.response.headers.set('Accept-Ranges', 'bytes');
    request.response.headers.set('Content-Length', contentLength.toString());
    if (rangeHeader != null) {
      request.response.headers.set('Content-Range', 'bytes $startByte-$endByte/$totalLength');
    }

    print('[Proxy] Trình phát yêu cầu: $startByte-$endByte');

    bool clientDisconnected = false;
    request.response.done.then((_) {
      clientDisconnected = true;
      print('[Proxy] Trình phát đã ngắt kết nối.');
    }).catchError((_) { clientDisconnected = true; });

    int currentByte = startByte;
    Map<int, Future<Uint8List?>> downloadTasks = {};

    Future<Uint8List?> _downloadChunk(int start, int end) async {
      print('  -> Đang tải: $start - $end');
      final chunkReq = http.Request('GET', Uri.parse(targetUrl));
      chunkReq.headers['User-Agent'] = 'okhttp/4.12.0';
      chunkReq.headers['Range'] = 'bytes=$start-$end';
      final res = await client.send(chunkReq);
      if (res.statusCode != 206 && res.statusCode != 200) {
        print('  [!] Lỗi chunk $start: HTTP ${res.statusCode}');
        return null;
      }
      final bytes = await res.stream.toBytes();
      print('  <- Xong: $start');
      return bytes;
    }

    while (currentByte <= endByte && !clientDisconnected) {
      while (downloadTasks.length < maxWorkers && currentByte <= endByte) {
        int fetchEnd = currentByte + chunkSize - 1;
        if (fetchEnd > endByte) fetchEnd = endByte;
        downloadTasks[currentByte] = _downloadChunk(currentByte, fetchEnd);
        currentByte = fetchEnd + 1;
      }

      if (downloadTasks.isEmpty) break;

      final nextStartByte = downloadTasks.keys.reduce((a, b) => a < b ? a : b);
      final task = downloadTasks.remove(nextStartByte)!;

      try {
        final data = await task;
        if (clientDisconnected) break;
        if (data == null) break; // Lỗi HTTP
        request.response.add(data);
        await request.response.flush();
      } catch (e) {
        print('[Proxy] Lỗi add data: $e');
        break;
      }
    }
    
    client.close();
    if (!clientDisconnected) {
      await request.response.close();
    }
  }
}

void main() async {
  await MultiThreadProxy.start();
  print("Đã bật Proxy. Bỏ link này vào VLC để test:");
  print("http://localhost:8081/?id=5QX97YWDVY1X");
}
