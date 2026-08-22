import re
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = '''if (name.contains('p2p') || name.contains('torrent')) {
          _p2pServers.add(server);
        } else if (name.contains('film4k archive')) {
          _vietsubServers.add(server); // Force Film4k into standard tab
        } else if (name.contains('premium') ||'''

text = text.replace('''if (name.contains('p2p') || name.contains('torrent')) {
          _p2pServers.add(server);
        } else if (name.contains('premium') ||''', replacement)

with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
