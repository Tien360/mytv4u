import re

def patch_playlist_limit(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where args is defined
    old_args = r"List<String> args = \['--dump-json', '--flat-playlist', url\];"
    new_args = '''List<String> args = ['--dump-json', '--flat-playlist', url];
      if (url.contains('list=RD')) {
        args.insert(0, '25');
        args.insert(0, '--playlist-end');
      }'''
        
    match = re.search(old_args, content, flags=re.MULTILINE)
    if match:
        content = content.replace(match.group(0), new_args)
    else:
        print("Could not find args block in " + filepath)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_playlist_limit('lib/screens/player_screen.dart')
patch_playlist_limit('lib/screens/library_screen.dart')
print("Patched playlist limit")
