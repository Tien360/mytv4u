import 'phim_api.dart';
import 'dart:convert';
import 'package:crypto/crypto.dart';
import 'package:encrypt/encrypt.dart' as encrypt;
import 'dart:typed_data';
import 'package:http/http.dart' as http;

class PremiumResolver {
  static final List<Map<String, String>> _servers = [
    {
      "name": "Server 1",
      "cdn": "https://sv1.p4k.dpdns.org",
      "secret": "5e8d1b4f9c2a6e730b1f8d4a92c5e3d1",
      "ua": "okhttp/4.12.0"
    },
    {
      "name": "Server 2",
      "cdn": "https://sv2.p4k.dpdns.org",
      "secret": "f7a2c8e1b5d493f0a6b2d9e8c1f3a5b4",
      "ua": "Dart/3.12 (dart:io)"
    }
  ];

  

  static Duration? _utcOffset;

    static Future<void> preload() async {
    await Future.wait([
      _getDynamicBaseDomain(),
      _preloadUtcOffset(),
      _preloadFree1Domain(),
    ]);
  }

  static Future<void> _preloadFree1Domain() async {
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
         
         PhimApi.free1Url = location;
         PhimApi.free1List = location + '/danh-sach';
      }
    } catch (_) {}
  }

  static Future<void> _preloadUtcOffset() async {
    try {
      final res = await http.get(Uri.parse('https://worldtimeapi.org/api/timezone/Etc/UTC')).timeout(const Duration(seconds: 3));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final serverUtc = DateTime.parse(data['utc_datetime']).toUtc();
        final localUtc = DateTime.now().toUtc();
        _utcOffset = serverUtc.difference(localUtc);
      }
    } catch (_) {}
  }

  static String? _dynamicBaseDomain;

  static Future<String?> _getDynamicBaseDomain() async {
    if (_dynamicBaseDomain != null) return _dynamicBaseDomain;
    try {
      final client = http.Client();
      final request = http.Request('GET', Uri.parse('https://rip.cryboiz.workers.dev/go/cdn'))
        ..followRedirects = false;
      final response = await client.send(request).timeout(const Duration(seconds: 5));
      
      String? location;
      if (response.statusCode == 301 || response.statusCode == 302 || response.statusCode == 307 || response.statusCode == 308) {
         location = response.headers['location'];
      }
      
      if (location != null && location.isNotEmpty) {
        final uri = Uri.parse(location);
        final host = uri.host;
        final parts = host.split('.');
        if (parts.length > 2) {
          _dynamicBaseDomain = parts.sublist(1).join('.');
          print('[PremiumResolver] Dynamic CDN Base Domain: $_dynamicBaseDomain');
          return _dynamicBaseDomain;
        }
      }
    } catch (e) {
      print('[PremiumResolver] Error fetching dynamic CDN: $e');
    }
    return null;
  }

  static DateTime _getUtcTime() {
    final now = DateTime.now().toUtc();
    if (_utcOffset != null) {
      return now.add(_utcOffset!);
    }
    return now;
  }

  static Future<List<String>> getVideoStream(String fileId) async {
    final utcDt = _getUtcTime();
    final int nowSec = (utcDt.millisecondsSinceEpoch / 1000).floor();

    final String dateStr = "${utcDt.year}${utcDt.month.toString().padLeft(2, '0')}${utcDt.day.toString().padLeft(2, '0')}";
    
    final dynamicBase = await _getDynamicBaseDomain();
    
    List<String> streams = [];
    for (var server in _servers) {
      try {
        final secret = server['secret']!;
        String cdn = server['cdn']!;
        if (dynamicBase != null) {
          final uri = Uri.parse(cdn);
          final svPrefix = uri.host.split('.').first;
          cdn = "${uri.scheme}://$svPrefix.$dynamicBase";
        }
        final ua = server['ua']!;
        
        final keyBytes = sha256.convert(utf8.encode(secret)).bytes;
        final ivFull = sha256.convert(utf8.encode('iv:' + secret)).bytes;
        final ivBytes = Uint8List.fromList(ivFull.sublist(0, 12));
        
        final plaintext = utf8.encode("$secret:$dateStr");
        final key = encrypt.Key(Uint8List.fromList(keyBytes));
        final iv = encrypt.IV(ivBytes);
        final encrypter = encrypt.Encrypter(encrypt.AES(key, mode: encrypt.AESMode.gcm));
        
        final encrypted = encrypter.encryptBytes(plaintext, iv: iv);
        final ciphertextHex = encrypted.bytes.map((b) => b.toRadixString(16).padLeft(2, '0')).join('');
        final signingSecret = "$secret:$ciphertextHex";
        
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
        
        final apiUrl = "$cdn/$fileId?token=$token&ts=$tsHex";
        
        final response = await http.get(
          Uri.parse(apiUrl), 
          headers: {'User-Agent': ua, 'Accept': '*/*'}
        ).timeout(const Duration(seconds: 10));
        
        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          final streamUrl = data['url']?.toString();
          
          if (streamUrl != null && streamUrl.isNotEmpty) {
            if (streamUrl.contains('dmm_vo_cc')) {
              print('[PremiumResolver] Honeypot detected on ${server['name']}');
              continue;
            }
            if (!streams.contains(streamUrl)) {
              streams.add(streamUrl);
            }
          }
        }
      } catch (e) {
        print("[PremiumResolver] Error on ${server['name']}: $e");
      }
    }
    return streams;
  }
}
