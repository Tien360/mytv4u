import re

with open('lib/services/deep_link_service.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Register context menus
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

      // 2. Register "Open with MyTV4U" context menu for media files
      final extensions = ['.mp4', '.mkv', '.avi', '.flv', '.webm', '.mov', '.ts', '.mp3', '.m4a', '.wav', '.flac', '.aac'];
      for (final ext in extensions) {
        await Process.run('cmd', ['/c', 'reg', 'add',
          'HKCU\\Software\\Classes\\SystemFileAssociations\\$ext\\shell\\OpenWithMyTV4U',
          '/ve', '/d', 'Mở bằng MyTV4U', '/f']);
        await Process.run('cmd', ['/c', 'reg', 'add',
          'HKCU\\Software\\Classes\\SystemFileAssociations\\$ext\\shell\\OpenWithMyTV4U\\command',
          '/ve', '/d', '"$exePath" "%1"', '/f']);
      }
      
      debugPrint('[DeepLink] Protocol & Context Menus registered -> $exePath');
"""

content = re.sub(r'    try \{\s*final exePath.*?(?=    \} catch \(e\))', lambda m: register_code, content, flags=re.DOTALL)

# Add file path parsing
parse_code = r"""
  void _parseLaunchArgs(List<String> args) {
    for (final arg in args) {
      if (arg.startsWith('mytv4u://')) {
        final data = _parseUri(arg);
        if (data != null) {
          initialDeepLink = data;
          debugPrint('[DeepLink] Launch deep link: ${data.action} slug=${data.slug}');
        }
        break;
      } else if (File(arg).existsSync()) {
        initialDeepLink = DeepLinkData(action: 'local_file', slug: arg, source: 'local');
        debugPrint('[DeepLink] Launch local file: $arg');
        break;
      }
    }
  }
"""

content = re.sub(r'  void _parseLaunchArgs.*?\}\n  \}', lambda m: parse_code, content, flags=re.DOTALL)

with open('lib/services/deep_link_service.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated deep_link_service.dart")
