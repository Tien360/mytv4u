import re

with open('lib/services/deep_link_service.dart', 'r', encoding='utf-8') as f:
    content = f.read()

register_code = r"""
    try {
      final exePath = Platform.resolvedExecutable;
      
      // 1. Register custom URL protocol
      await Process.run('cmd', ['/c', 'reg', 'add',
        r'HKCU\Software\Classes\mytv4u',
        '/ve', '/d', 'URL:MyTV4u Protocol', '/f']);
      await Process.run('cmd', ['/c', 'reg', 'add',
        r'HKCU\Software\Classes\mytv4u',
        '/v', 'URL Protocol', '/d', '', '/f']);
      await Process.run('cmd', ['/c', 'reg', 'add',
        r'HKCU\Software\Classes\mytv4u\shell\open\command',
        '/ve', '/d', '"$exePath" "%1"', '/f']);

      // 2. Register ProgID for "Open With"
      const progId = 'MyTV4U.MediaFile';
      await Process.run('cmd', ['/c', 'reg', 'add',
        'HKCU\\Software\\Classes\\$progId',
        '/ve', '/d', 'MyTV4U Media File', '/f']);
      await Process.run('cmd', ['/c', 'reg', 'add',
        'HKCU\\Software\\Classes\\$progId\\shell\\open\\command',
        '/ve', '/d', '"$exePath" "%1"', '/f']);

      // 3. Register Applications for "Open With" (Modern Windows)
      final exeName = exePath.split('\\').last;
      await Process.run('cmd', ['/c', 'reg', 'add',
        'HKCU\\Software\\Classes\\Applications\\$exeName\\shell\\open\\command',
        '/ve', '/d', '"$exePath" "%1"', '/f']);

      // 4. Add to OpenWithProgids for each extension
      final extensions = ['.mp4', '.mkv', '.avi', '.flv', '.webm', '.mov', '.ts', '.mp3', '.m4a', '.wav', '.flac', '.aac'];
      for (final ext in extensions) {
        // Add to OpenWithProgids
        await Process.run('cmd', ['/c', 'reg', 'add',
          'HKCU\\Software\\Classes\\$ext\\OpenWithProgids',
          '/v', progId, '/d', '', '/f']);
        
        // Declare SupportedTypes in Applications
        await Process.run('cmd', ['/c', 'reg', 'add',
          'HKCU\\Software\\Classes\\Applications\\$exeName\\SupportedTypes',
          '/v', ext, '/d', '', '/f']);
      }
      
      debugPrint('[DeepLink] Protocol & Context Menus registered -> $exePath');
"""

content = re.sub(r'    try \{\s*final exePath.*?(?=    \} catch \(e\))', lambda m: register_code, content, flags=re.DOTALL)

with open('lib/services/deep_link_service.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated deep_link_service.dart again")
