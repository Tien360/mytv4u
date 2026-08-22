import re

with open('lib/services/deep_link_service.dart', 'r', encoding='utf-8') as f:
    content = f.read()

register_code = r"""
    try {
      final exePath = Platform.resolvedExecutable;
      final exeDir = File(exePath).parent.path;
      final audioIcoPath = '$exeDir\\audio.ico';
      
      // 1. Register custom URL protocol
      await Process.run('cmd', ['/c', 'reg', 'add', r'HKCU\Software\Classes\mytv4u', '/ve', '/d', 'URL:MyTV4u Protocol', '/f']);
      await Process.run('cmd', ['/c', 'reg', 'add', r'HKCU\Software\Classes\mytv4u', '/v', 'URL Protocol', '/d', '', '/f']);
      await Process.run('cmd', ['/c', 'reg', 'add', r'HKCU\Software\Classes\mytv4u\shell\open\command', '/ve', '/d', '"$exePath" "%1"', '/f']);

      // 2. Register ProgIDs for "Open With" and Default Icons
      const videoProgId = 'MyTV4U.VideoFile';
      await Process.run('cmd', ['/c', 'reg', 'add', 'HKCU\\Software\\Classes\\$videoProgId', '/ve', '/d', 'MyTV4U Video File', '/f']);
      // For video, we set DefaultIcon to the exe, Windows will generate a thumbnail and put the exe icon in the corner!
      await Process.run('cmd', ['/c', 'reg', 'add', 'HKCU\\Software\\Classes\\$videoProgId\\DefaultIcon', '/ve', '/d', '"$exePath",0', '/f']);
      await Process.run('cmd', ['/c', 'reg', 'add', 'HKCU\\Software\\Classes\\$videoProgId\\shell\\open\\command', '/ve', '/d', '"$exePath" "%1"', '/f']);

      const audioProgId = 'MyTV4U.AudioFile';
      await Process.run('cmd', ['/c', 'reg', 'add', 'HKCU\\Software\\Classes\\$audioProgId', '/ve', '/d', 'MyTV4U Audio File', '/f']);
      // For audio, we use the custom audio.ico we generated
      await Process.run('cmd', ['/c', 'reg', 'add', 'HKCU\\Software\\Classes\\$audioProgId\\DefaultIcon', '/ve', '/d', '"$audioIcoPath"', '/f']);
      await Process.run('cmd', ['/c', 'reg', 'add', 'HKCU\\Software\\Classes\\$audioProgId\\shell\\open\\command', '/ve', '/d', '"$exePath" "%1"', '/f']);

      // 3. Register Applications for "Open With" (Modern Windows)
      final exeName = exePath.split('\\').last;
      await Process.run('cmd', ['/c', 'reg', 'add', 'HKCU\\Software\\Classes\\Applications\\$exeName\\shell\\open\\command', '/ve', '/d', '"$exePath" "%1"', '/f']);

      // 4. Add to OpenWithProgids for each extension
      final videoExts = ['.mp4', '.mkv', '.avi', '.flv', '.webm', '.mov', '.ts'];
      final audioExts = ['.mp3', '.m4a', '.wav', '.flac', '.aac'];

      for (final ext in videoExts) {
        await Process.run('cmd', ['/c', 'reg', 'add', 'HKCU\\Software\\Classes\\$ext\\OpenWithProgids', '/v', videoProgId, '/d', '', '/f']);
        await Process.run('cmd', ['/c', 'reg', 'add', 'HKCU\\Software\\Classes\\Applications\\$exeName\\SupportedTypes', '/v', ext, '/d', '', '/f']);
      }
      for (final ext in audioExts) {
        await Process.run('cmd', ['/c', 'reg', 'add', 'HKCU\\Software\\Classes\\$ext\\OpenWithProgids', '/v', audioProgId, '/d', '', '/f']);
        await Process.run('cmd', ['/c', 'reg', 'add', 'HKCU\\Software\\Classes\\Applications\\$exeName\\SupportedTypes', '/v', ext, '/d', '', '/f']);
      }
      
      // Notify Windows Explorer to refresh icons
      // await Process.run('cmd', ['/c', 'ie4uinit.exe', '-show']);
      
      debugPrint('[DeepLink] Protocol & Context Menus registered -> $exePath');
"""

content = re.sub(r'    try \{\s*final exePath.*?(?=    \} catch \(e\))', lambda m: register_code, content, flags=re.DOTALL)

with open('lib/services/deep_link_service.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated deep_link_service.dart for icons")
