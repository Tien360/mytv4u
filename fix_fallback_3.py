import re

def fix_fallback_logic(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the fallback block
    old_fallback = r"ProcessResult res = await Process\.run\(exePath, args\);\s*// FALLBACK if cookie extraction fails\s*if \(res\.exitCode != 0 && isYtLinked\) \{\s*debugPrint\('Cookie extraction failed\. Retrying without cookies\.\.\.'\);\s*res = await Process\.run\(exePath, \['--dump-json', '--flat-playlist', url\]\);\s*\}\s*if \(res\.exitCode == 0\) \{"
    
    new_fallback = '''ProcessResult res = await Process.run(exePath, args);
      
      // yt-dlp might return exitCode 1 if some videos in the playlist are hidden/unavailable
      // So we should check if stdout has content instead of strictly checking exitCode 0
      if (res.stdout.toString().trim().isEmpty && isYtLinked) {
        debugPrint('Cookie extraction failed or empty. Retrying without cookies...');
        res = await Process.run(exePath, ['--dump-json', '--flat-playlist', url]);
      }

      if (res.stdout.toString().trim().isNotEmpty) {'''
        
    match = re.search(old_fallback, content, flags=re.MULTILINE)
    if match:
        content = content.replace(match.group(0), new_fallback)
    else:
        print("Could not find fallback block in player_screen")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_fallback_logic('lib/screens/player_screen.dart')
print("Patched player_screen.dart fallback logic")
