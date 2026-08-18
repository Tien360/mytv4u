import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Add vidsrc and vidapi to _sources map
old_sources = '''    'motchill': true,
    'torrentio': false, // Torrent is experimental, default to off
  };'''
new_sources = '''    'motchill': true,
    'torrentio': false,
    'vidsrc': true,
    'vidapi': true,
  };'''
content = content.replace(old_sources, new_sources)

# Add them to the UI
# There's a list of source titles:
# 'free1': 'Free1', 'motchill': 'Motchill', 'torrentio': 'Torrent (P2P)'
old_titles = '''            'motchill': 'Motchill (Tuá»³ chá» n)',
            'torrentio': 'Torrent (Thá»­ nghiá»‡m)',
          };'''
new_titles = '''            'motchill': 'Motchill (Tuá»³ chá» n)',
            'torrentio': 'Torrent (Thá»­ nghiá»‡m)',
            'vidsrc': 'VidSrc (Server nhúng)',
            'vidapi': 'VidAPI (Server nhúng)',
          };'''
content = content.replace(old_titles, new_titles)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched settings_screen.dart for sources')
