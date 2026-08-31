import re

def fix_fallback_logic(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the fallback block in library_screen.dart
    old_fallback = r"ProcessResult res = await Process\.run\(exePath, args\);\s*if \(res\.exitCode != 0 && isYtLinked\) \{\s*// Fallback\s*res = await Process\.run\(exePath, \['--dump-json', '--flat-playlist', url\]\);\s*\}\s*if \(res\.exitCode == 0\) \{"
    
    new_fallback = '''ProcessResult res = await Process.run(exePath, args);
                                if (res.stdout.toString().trim().isEmpty && isYtLinked) {
                                  // Fallback
                                  res = await Process.run(exePath, ['--dump-json', '--flat-playlist', url]);
                                }
                                
                                if (res.stdout.toString().trim().isNotEmpty) {'''
        
    match = re.search(old_fallback, content, flags=re.MULTILINE)
    if match:
        content = content.replace(match.group(0), new_fallback)
    else:
        print("Could not find fallback block in library_screen")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_fallback_logic('lib/screens/library_screen.dart')
print("Patched library_screen.dart fallback logic")
