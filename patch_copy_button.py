import sys

file_path = 'lib/screens/player_screen.dart'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """                              if (_isUsingWebview)
                                _buildInfoRow('URL', _currentUrl),"""

replacement = """                              if (_isUsingWebview)
                                _buildInfoRow('URL', _currentUrl)
                              else
                                Padding(
                                  padding: const EdgeInsets.only(top: 8.0, bottom: 16.0),
                                  child: ElevatedButton.icon(
                                    icon: const Icon(Icons.copy, size: 16),
                                    label: const Text('Sao chép link luồng (External Player)'),
                                    onPressed: () {
                                      Clipboard.setData(ClipboardData(text: _currentUrl));
                                      ScaffoldMessenger.of(context).showSnackBar(
                                        const SnackBar(content: Text('Đã sao chép link phát!')),
                                      );
                                    },
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: Colors.white24,
                                      foregroundColor: Colors.white,
                                      elevation: 0,
                                    ),
                                  ),
                                ),"""

if target in content:
    new_content = content.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patched!")
else:
    print("Target not found")
    # let's try a regex approach
    import re
    match = re.search(r"if \(_isUsingWebview\)\s*_buildInfoRow\('URL', _currentUrl\),", content)
    if match:
        new_content = content[:match.start()] + replacement + content[match.end():]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Patched with regex!")
    else:
        print("Still not found!")
