import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'auto_translate.dart';

void main(List<String> args) async {
  if (args.length < 2) {
    print('SÃ¡Â»Â­ dÃ¡Â»Â¥ng: dart run tools/release.dart <version> "<release_notes>"');
    print('VÃƒÂ­ dÃ¡Â»Â¥: dart run tools/release.dart 26.08.09.a.public "TÃƒÂ­nh nÃ„Æ’ng mÃ¡Â»â€ºi A, B"');
    exit(1);
  }

  final version = args[0];
  final notes = args[1];

  print('=============================================');
  print('Ã°Å¸Å¡â‚¬ TIÃ¡ÂºÂ¾N TRÃƒÅ’NH PHÃƒÂT HÃƒâ‚¬NH TÃ¡Â»Â° Ã„ÂÃ¡Â»ËœNG MyTV4U');
  print('=============================================');
  print('PhiÃƒÂªn bÃ¡ÂºÂ£n: $version');
  print('NÃ¡Â»â„¢i dung: $notes\n');

  await autoTranslate();

  // 1. CÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t lib/api/update_api.dart
  print('[1/6] Ã„Âang cÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t mÃƒÂ£ nguÃ¡Â»â€œn Dart...');
  final updateApiFile = File('lib/api/update_api.dart');
  if (updateApiFile.existsSync()) {
    String content = updateApiFile.readAsStringSync();
    content = content.replaceAll(
      RegExp(r"static const String currentAppVersion = '.*';"),
      "static const String currentAppVersion = '$version';"
    );
    updateApiFile.writeAsStringSync(content);
    print('  -> Ã„ÂÃƒÂ£ sÃ¡Â»Â­a update_api.dart');
  } else {
    print('  -> KHÃƒâ€NG TÃƒÅ’M THÃ¡ÂºÂ¤Y lib/api/update_api.dart');
    exit(1);
  }

  // 2. CÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t installer.iss
  print('[2/6] Ã„Âang cÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t kÃ¡Â»â€¹ch bÃ¡ÂºÂ£n Ã„â€˜ÃƒÂ³ng gÃƒÂ³i Inno Setup...');
  final issFile = File('installer.iss');
  if (issFile.existsSync()) {
    String content = issFile.readAsStringSync();
    content = content.replaceAll(
      RegExp(r"AppVersion=.*"),
      "AppVersion=$version"
    );
    // Thay Ã„â€˜Ã¡Â»â€¢i Ã„â€˜Ã†Â°Ã¡Â»Âng dÃ¡ÂºÂ«n xuÃ¡ÂºÂ¥t file vÃƒÂ o thÃ†Â° mÃ¡Â»Â¥c Releases/vXXX Ã„â€˜Ã¡Â»Æ’ gÃ¡Â»Ân
    content = content.replaceAll(
      RegExp(r"OutputDir=.*"),
      "OutputDir=T:\\Project\\Phim\\mytv4u_flutter\\Releases\\v$version"
    );
    content = content.replaceAll(
      RegExp(r"OutputBaseFilename=.*"),
      "OutputBaseFilename=MyTV4U_Setup_$version"
    );
    issFile.writeAsStringSync(content);
    print('  -> Ã„ÂÃƒÂ£ sÃ¡Â»Â­a installer.iss');
  }

  // 3. ChÃ¡ÂºÂ¡y Flutter Build
  print('[3/6] Ã„Âang chÃ¡ÂºÂ¡y Flutter Build...');
  final buildProcess = await Process.start('flutter', ['build', 'windows', '--verbose', '--no-pub'], runInShell: true);
  buildProcess.stdout.listen(stdout.add);
    buildProcess.stderr.listen(stderr.add);
  final buildCode = await buildProcess.exitCode;
  if (buildCode != 0) {
    print('  -> LÃ¡Â»â€“I BIÃƒÅ N DÃ¡Â»Å CH FLUTTER!');
    exit(1);
  }
  print('  -> BiÃªn dá»‹ch thÃ nh cÃ´ng.');

  // Thay tháº¿ libmpv-2.dll náº¿u cÃ³ báº£n custom (Ä‘áº§y Ä‘á»§ codec)
  final customMpv = File('windows/libmpv-2.dll');
  if (customMpv.existsSync()) {
    print('  -> PhÃ¡t hiá»‡n báº£n libmpv-2.dll tÃ¹y chá»‰nh. Äang ghi Ä‘Ã¨ báº£n máº·c Ä‘á»‹nh...');
    final releaseMpv = File('build/windows/x64/runner/Release/libmpv-2.dll');
    if (releaseMpv.existsSync()) {
      customMpv.copySync(releaseMpv.path);
      print('  -> ÄÃ£ ghi Ä‘Ã¨ libmpv-2.dll thÃ nh cÃ´ng!');
    }
  }

  // ÄÃ³ng gÃ³i Custom Node.js Torrent Engine
  print('  -> Äang sao chÃ©p LÃµi Torrent Custom vÃ o báº£n Build...');
  final torrentDir = Directory('stremio_server');
  if (torrentDir.existsSync()) {
    await Process.run('xcopy', ['stremio_server', 'build\\windows\\x64\\runner\\Release\\stremio_server', '/E', '/I', '/Y']);
    print('  -> ÄÃ£ sao chÃ©p LÃµi Torrent thÃ nh cÃ´ng!');
  }

  print('  -> Äang sao chÃ©p tv_web_player...');
  final tvWebPlayerDir = Directory(r'..\tv_web_player\bin\Release\net8.0-windows\win-x64\publish');
  if (tvWebPlayerDir.existsSync()) {
    await Process.run('xcopy', [r'..\tv_web_player\bin\Release\net8.0-windows\win-x64\publish\*', r'build\windows\x64\runner\Release\', '/E', '/I', '/Y']);
    print('  -> ÄÃ£ sao chÃ©p tv_web_player thÃ nh cÃ´ng!');
  }

  // 4. ÄÃ³ng gÃ³i Inno Setup
  print('[4/6] Äang Ä‘Ã³ng gÃ³i file Setup.exe báº±ng Inno Setup...');
  final userProfile = Platform.environment['USERPROFILE'];
  final isccPath = '$userProfile\\AppData\\Local\\Programs\\Inno Setup 6\\ISCC.exe';
  
  if (File(isccPath).existsSync()) {
    final isccProcess = await Process.start(isccPath, ['installer.iss'], runInShell: true);
    isccProcess.stdout.listen(stdout.add);
      isccProcess.stderr.listen(stderr.add);
    final isccCode = await isccProcess.exitCode;
    if (isccCode != 0) {
      print('  -> LÃ¡Â»â€“I Ã„ÂÃƒâ€œNG GÃƒâ€œI INNO SETUP!');
      exit(1);
    }
    print('  -> Ã„ÂÃƒÂ³ng gÃƒÂ³i thÃƒÂ nh cÃƒÂ´ng.');
  } else {
    print('  -> KHÃƒâ€NG TÃƒÅ’M THÃ¡ÂºÂ¤Y ISCC.exe TÃ¡ÂºÂ I $isccPath');
    exit(1);
  }

  // 5. QuÃ„Æ’ng lÃƒÂªn GitHub
  print('[5/6] Ã„Âang Ã„â€˜Ã¡ÂºÂ©y lÃƒÂªn GitHub...');
  print('[5/6] Ã„ ang Ã„â€˜Ã¡ÂºÂ©y lÃƒÂªn GitHub...');
  final setupExePath = 'Releases\\v$version\\MyTV4U_Setup_$version.exe';
  final ghPath = 'gh';
  if (File(ghPath).existsSync()) {
    bool isBeta = version.contains('.beta');
    List<String> ghArgs = [
      'release', 'create', version, setupExePath, 
      '--title', 'PhiÃªn báº£n $version', 
      '--notes', notes,
      '--target', 'master'
    ];
    if (isBeta) {
      ghArgs.add('--prerelease');
    }
    
    final ghProcess = await Process.start(
      ghPath, 
      ghArgs,
      runInShell: true
    );
    ghProcess.stdout.listen(stdout.add);
      ghProcess.stderr.listen(stderr.add);
    final ghCode = await ghProcess.exitCode;
    if (ghCode != 0) {
      print('  -> LÃ¡Â»â€“I Ã„ÂÃ¡ÂºÂ¨Y LÃƒÅ N GITHUB!');
      exit(1);
    }
    print('  -> TÃ¡ÂºÂ£i lÃƒÂªn GitHub thÃƒÂ nh cÃƒÂ´ng.');
  } else {
    print('  -> KHÃƒâ€NG TÃƒÅ’M THÃ¡ÂºÂ¤Y GitHub CLI TÃ¡ÂºÂ I $ghPath');
    exit(1);
  }

  // 6. CÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t Firebase
  print('[6/6] Ã„Âang cÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t Ã„â€˜Ã†Â°Ã¡Â»Âng link lÃƒÂªn Firebase...');
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
      print('  -> CÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t Firebase ($channel) thÃƒÂ nh cÃƒÂ´ng!');
      
      // NÃ¡ÂºÂ¿u lÃƒÂ  bÃ¡ÂºÂ£n public, cÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t thÃƒÂªm updates/latest cho cÃƒÂ¡c bÃ¡ÂºÂ£n cÃ…Â© (bÃ¡ÂºÂ£n C trÃ¡Â»Å¸ vÃ¡Â»Â trÃ†Â°Ã¡Â»â€ºc)
      if (channel == 'public') {
        final latestUrl = Uri.parse('https://firestore.googleapis.com/v1/projects/tv4u-ec4ae/databases/(default)/documents/updates/latest');
        final latestRes = await http.patch(
          latestUrl, 
          headers: {'Content-Type': 'application/json; charset=UTF-8'},
          body: json.encode(body)
        );
        if (latestRes.statusCode == 200) {
          print('  -> Ã„ÂÃƒÂ£ cÃ¡ÂºÂ­p nhÃ¡ÂºÂ­t thÃƒÂªm kÃƒÂªnh updates/latest cho phiÃƒÂªn bÃ¡ÂºÂ£n cÃ…Â©!');
        }
      }
    } else {
      print('  -> LÃ¡Â»â€”i Firebase: ${res.statusCode} ${res.body}');
    }
  } catch(e) {
    print('  -> LÃ¡Â»â€”i kÃ¡ÂºÂ¿t nÃ¡Â»â€˜i Firebase: $e');
  }

  print('\n=============================================');
  print('Ã°Å¸Å½â€° Ã„ÂÃƒÆ’ HOÃƒâ‚¬N TÃ¡ÂºÂ¤T TOÃƒâ‚¬N BÃ¡Â»Ëœ QUÃƒÂ TRÃƒÅ’NH PHÃƒÂT HÃƒâ‚¬NH! Ã°Å¸Å½â€°');
  print('Ã„ÂÃ†Â°Ã¡Â»Âng dÃ¡ÂºÂ«n file: $setupExePath');
  print('=============================================');
}

