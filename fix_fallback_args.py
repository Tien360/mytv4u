import re

def fix_fallback_args(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the fallback block
    old_fallback = r"res = await Process\.run\(exePath, \['--dump-json', '--flat-playlist', url\]\);"
    
    new_fallback = '''
        List<String> fallbackArgs = ['--dump-json', '--flat-playlist', url];
        if (url.contains('list=RD')) {
          fallbackArgs.insert(0, '25');
          fallbackArgs.insert(0, '--playlist-end');
        }
        res = await Process.run(exePath, fallbackArgs);'''
        
    match = re.search(old_fallback, content, flags=re.MULTILINE)
    if match:
        content = content.replace(match.group(0), new_fallback)
    else:
        print("Could not find fallback block in " + filepath)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_fallback_args('lib/screens/player_screen.dart')
fix_fallback_args('lib/screens/library_screen.dart')
print("Patched fallback args")
