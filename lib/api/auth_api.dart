import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:url_launcher/url_launcher.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthApi {
  static const String _htmlContent = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Đăng nhập TV4U</title>
  <style>
    body { background-color: #1a1a1a; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    button { padding: 12px 24px; font-size: 18px; cursor: pointer; border-radius: 8px; border: none; background: white; color: black; font-weight: bold; }
    button:hover { background: #ddd; }
  </style>
  <script type="module">
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
    import { getAuth, signInWithPopup, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

    const firebaseConfig = {
      apiKey: "AIzaSyB9-OylVieBa87Z3WwOjsWY18r0ZFmlHt8",
      authDomain: "tv4u-ec4ae.firebaseapp.com",
      projectId: "tv4u-ec4ae",
      storageBucket: "tv4u-ec4ae.firebasestorage.app",
      messagingSenderId: "1046988652276",
      appId: "1:1046988652276:web:70cf98fef584df0e1568a1"
    };

    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);
    const provider = new GoogleAuthProvider();

    window.login = async () => {
      try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        const uid = user.uid;
        const displayName = user.displayName;
        const photoURL = user.photoURL;
        
        document.body.innerHTML = '<h2>Đăng nhập thành công! Bạn có thể đóng tab này và quay lại ứng dụng.</h2>';
        
        await fetch('/token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ uid, displayName, photoURL })
        });
        
        setTimeout(() => window.close(), 2000);
      } catch (e) {
        alert("Lỗi đăng nhập: " + e.message);
      }
    };
  </script>
</head>
<body>
  <h2>Đăng nhập để đồng bộ với TV4U</h2>
  <button onclick="login()">Đăng nhập với Google</button>
</body>
</html>
''';

  static Future<Map<String, String>?> loginWithGoogle() async {
    final completer = Completer<Map<String, String>?>();
    HttpServer? server;

    try {
      server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
      final port = server.port;
      // Firebase Auth whitelists 'localhost' by default, not '127.0.0.1'
      final url = 'http://localhost:$port/';
      
      server.listen((HttpRequest request) async {
        // Cấu hình CORS để chắc chắn không bị block
        request.response.headers.add('Access-Control-Allow-Origin', '*');
        request.response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
        request.response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');

        if (request.method == 'OPTIONS') {
          request.response.statusCode = HttpStatus.ok;
          await request.response.close();
          return;
        }

        if (request.uri.path == '/') {
          request.response
            ..headers.contentType = ContentType.html
            ..write(_htmlContent);
          await request.response.close();
        } else if (request.uri.path == '/token' && request.method == 'POST') {
          try {
            final body = await utf8.decoder.bind(request).join();
            final data = jsonDecode(body) as Map<String, dynamic>;
            
            final uid = data['uid']?.toString() ?? '';
            final displayName = data['displayName']?.toString() ?? '';
            final photoURL = data['photoURL']?.toString() ?? '';

            if (uid.isNotEmpty) {
              final prefs = await SharedPreferences.getInstance();
              await prefs.setString('firebase_uid', uid);
              await prefs.setString('user_name', displayName);
              await prefs.setString('user_avatar', photoURL);

              if (!completer.isCompleted) {
                completer.complete({
                  'uid': uid,
                  'displayName': displayName,
                  'photoURL': photoURL,
                });
              }
            }
          } catch (e) {
            print('Error parsing token: $e');
          }
          request.response.statusCode = HttpStatus.ok;
          await request.response.close();
        } else {
          request.response.statusCode = HttpStatus.notFound;
          await request.response.close();
        }
      });

      if (await canLaunchUrl(Uri.parse(url))) {
        await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
      } else {
        throw Exception('Could not launch browser');
      }

      // Timeout sau 2 phút nếu người dùng không thao tác
      Timer(const Duration(minutes: 2), () {
        if (!completer.isCompleted) {
          completer.complete(null);
        }
      });

      final result = await completer.future;
      await server.close(force: true);
      return result;

    } catch (e) {
      if (server != null) {
        await server.close(force: true);
      }
      if (!completer.isCompleted) {
        completer.complete(null);
      }
      return null;
    }
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('firebase_uid');
    await prefs.remove('user_name');
    await prefs.remove('user_avatar');
  }

  static Future<Map<String, String>?> getCurrentUser() async {
    final prefs = await SharedPreferences.getInstance();
    final uid = prefs.getString('firebase_uid');
    if (uid == null || uid.startsWith('anon_')) return null;

    return {
      'uid': uid,
      'displayName': prefs.getString('user_name') ?? '',
      'photoURL': prefs.getString('user_avatar') ?? '',
    };
  }
}
