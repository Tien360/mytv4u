import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'auto_translate.dart';

void main(List<String> args) async {
  if (args.length < 2) {
    print('Sá»­ dá»¥ng: dart run tools/release.dart <version> "<release_notes>"');
    print('VÃ­ dá»¥: dart run tools/release.dart 26.08.09.a.public "TÃ­nh nÄƒng má»›i A, B"');
    exit(1);
  }

  final version = args[0];
  final notes = args[1];

  print('=============================================');
  print('ðŸš€ TIáº¾N TRÃŒNH PHÃT HÃ€NH Tá»° Äá»˜NG MyTV4U');
  print('=============================================');
  print('PhiÃªn báº£n: $version');
  print('Ná»™i dung: $notes\n');

  await autoTranslate();

  // 1. Cáº­p nháº­t lib/api/update_api.dart
  print('[1/6] Äang cáº­p nháº­t mÃ£ nguá»“n Dart...');
  final updateApiFile = File('lib/api/update_api.dart');
  if (updateApiFile.existsSync()) {
    String content = updateApiFile.readAsStringSync();
    content = content.replaceAll(
      RegExp(r"static const String currentAppVersion = '.*';"),
      "static const String currentAppVersion = '$version';"
    );
    updateApiFile.writeAsStringSync(content);
    print('  -> ÄÃ£ sá»­a update_api.dart');
  } else {
    print('  -> KHÃ”NG TÃŒM THáº¤Y lib/api/update_api.dart');
    exit(1);
  }

  // 2. Cáº­p nháº­t installer.iss
  print('[2/6] Äang cáº­p nháº­t ká»‹ch báº£n Ä‘Ã³ng gÃ³i Inno Setup...');
  final issFile = File('installer.iss');
  if (issFile.existsSync()) {
    String content = issFile.readAsStringSync();
    content = content.replaceAll(
      RegExp(r"AppVersion=.*"),
      "AppVersion=$version"
    );
    // Thay Ä‘á»•i Ä‘Æ°á»ng dáº«n xuáº¥t file vÃ o thÆ° má»¥c Releases/vXXX Ä‘á»ƒ gá»n
    content = content.replaceAll(
      RegExp(r"OutputDir=.*"),
      "OutputDir=T:\\Project\\Phim\\mytv4u_flutter\\Releases\\v$version"
    );
    content = content.replaceAll(
      RegExp(r"OutputBaseFilename=.*"),
      "OutputBaseFilename=MyTV4U_Setup_$version"
    );
    issFile.writeAsStringSync(content);
    print('  -> ÄÃ£ sá»­a installer.iss');
  }

  // 3. Cháº¡y Flutter Build
  print('[3/6] Äang cháº¡y Flutter Build...');
  final buildProcess = await Process.start('flutter', ['build', 'windows', '--no-pub'], runInShell: true);
  await stdout.addStream(buildProcess.stdout);
  await stderr.addStream(buildProcess.stderr);
  final buildCode = await buildProcess.exitCode;
  if (buildCode != 0) {
    print('  -> Lá»–I BIÃŠN Dá»ŠCH FLUTTER!');
    exit(1);
  }
  print('  -> Biên dịch thành công.');

  // Thay thế libmpv-2.dll nếu có bản custom (đầy đủ codec)
  final customMpv = File('windows/libmpv-2.dll');
  if (customMpv.existsSync()) {
    print('  -> Phát hiện bản libmpv-2.dll tùy chỉnh. Đang ghi đè bản mặc định...');
    final releaseMpv = File('build/windows/x64/runner/Release/libmpv-2.dll');
    if (releaseMpv.existsSync()) {
      customMpv.copySync(releaseMpv.path);
      print('  -> Đã ghi đè libmpv-2.dll thành công!');
    }
  }

  // Đóng gói Custom Node.js Torrent Engine
  print('  -> Đang sao chép Lõi Torrent Custom vào bản Build...');
  final torrentDir = Directory('stremio_server');
  if (torrentDir.existsSync()) {
    await Process.run('xcopy', ['stremio_server', 'build\\windows\\x64\\runner\\Release\\stremio_server', '/E', '/I', '/Y']);
    print('  -> Đã sao chép Lõi Torrent thành công!');
  }

  // 4. Đóng gói Inno Setup
  print('[4/6] Đang đóng gói file Setup.exe bằng Inno Setup...');
  final userProfile = Platform.environment['USERPROFILE'];
  final isccPath = '$userProfile\\AppData\\Local\\Programs\\Inno Setup 6\\ISCC.exe';
  
  if (File(isccPath).existsSync()) {
    final isccProcess = await Process.start(isccPath, ['installer.iss'], runInShell: true);
    await stdout.addStream(isccProcess.stdout);
    final isccCode = await isccProcess.exitCode;
    if (isccCode != 0) {
      print('  -> Lá»–I ÄÃ“NG GÃ“I INNO SETUP!');
      exit(1);
    }
    print('  -> ÄÃ³ng gÃ³i thÃ nh cÃ´ng.');
  } else {
    print('  -> KHÃ”NG TÃŒM THáº¤Y ISCC.exe Táº I $isccPath');
    exit(1);
  }

  // 5. QuÄƒng lÃªn GitHub
  print('[5/6] Äang Ä‘áº©y lÃªn GitHub...');
  final setupExePath = 'Releases\\v$version\\MyTV4U_Setup_$version.exe';
  final ghPath = 'C:\\Program Files\\GitHub CLI\\gh.exe';
  if (File(ghPath).existsSync()) {
    bool isBeta = version.contains('.beta');
    List<String> ghArgs = [
      'release', 'create', version, setupExePath, 
      '--title', 'PhiÃªn báº£n $version', 
      '--notes', notes
    ];
    if (isBeta) {
      ghArgs.add('--prerelease');
    }
    
    final ghProcess = await Process.start(
      ghPath, 
      ghArgs,
      runInShell: true
    );
    await stdout.addStream(ghProcess.stdout);
    final ghCode = await ghProcess.exitCode;
    if (ghCode != 0) {
      print('  -> Lá»–I Äáº¨Y LÃŠN GITHUB!');
      exit(1);
    }
    print('  -> Táº£i lÃªn GitHub thÃ nh cÃ´ng.');
  } else {
    print('  -> KHÃ”NG TÃŒM THáº¤Y GitHub CLI Táº I $ghPath');
    exit(1);
  }

  // 6. Cáº­p nháº­t Firebase
  print('[6/6] Äang cáº­p nháº­t Ä‘Æ°á»ng link lÃªn Firebase...');
  String channel = 'public';
  if (version.contains('.beta')) channel = 'beta';
  if (version.contains('.dev')) channel = 'dev';

  final url = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/$channel');
  final body = {
    "fields": {
      "latest_version": {"stringValue": version},
      "download_url": {"stringValue": "https://github.com/Tien360/mytv4u/releases/download/$version/MyTV4U_Setup_$version.exe"},
      "release_notes": {"stringValue": notes},
      "is_force_update": {"booleanValue": true}
    }
  };
  
  try {
    final res = await http.patch(
      url, 
      headers: {'Content-Type': 'application/json; charset=UTF-8'},
      body: json.encode(body)
    );
    if (res.statusCode == 200) {
      print('  -> Cáº­p nháº­t Firebase ($channel) thÃ nh cÃ´ng!');
      
      // Náº¿u lÃ  báº£n public, cáº­p nháº­t thÃªm updates/latest cho cÃ¡c báº£n cÅ© (báº£n C trá»Ÿ vá» trÆ°á»›c)
      if (channel == 'public') {
        final latestUrl = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/latest');
        final latestRes = await http.patch(
          latestUrl, 
          headers: {'Content-Type': 'application/json; charset=UTF-8'},
          body: json.encode(body)
        );
        if (latestRes.statusCode == 200) {
          print('  -> ÄÃ£ cáº­p nháº­t thÃªm kÃªnh updates/latest cho phiÃªn báº£n cÅ©!');
        }
      }
    } else {
      print('  -> Lá»—i Firebase: ${res.statusCode} ${res.body}');
    }
  } catch(e) {
    print('  -> Lá»—i káº¿t ná»‘i Firebase: $e');
  }

  print('\n=============================================');
  print('ðŸŽ‰ ÄÃƒ HOÃ€N Táº¤T TOÃ€N Bá»˜ QUÃ TRÃŒNH PHÃT HÃ€NH! ðŸŽ‰');
  print('ÄÆ°á»ng dáº«n file: $setupExePath');
  print('=============================================');
}
