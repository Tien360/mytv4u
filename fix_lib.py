import re

def fix_lib(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_code = """                        if (url.isNotEmpty) {
                          Navigator.pop(context);
                          Navigator.push("""
                          
    new_code = """                        if (url.isNotEmpty) {
                          if (url.contains('youtube.com') || url.contains('youtu.be')) {
                              bool isPlaylist = url.contains('list=') || url.contains('playlist?');
                              String vId = '';
                              try {
                                final uri = Uri.parse(url);
                                vId = uri.queryParameters['v'] ?? '';
                              } catch (e) {}
                              
                              if (vId.isEmpty && url.contains('youtu.be/')) {
                                vId = url.split('youtu.be/').last.split('?').first;
                              }
                              
                              if (vId.isEmpty) vId = url;

                              List<Episode> eps = [];
                              eps.add(Episode(
                                name: isPlaylist ? 'YouTube Playlist' : 'YouTube Video',
                                slug: vId,
                                m3u8Url: 'https://www.youtube.com/watch?v=$vId', // media_kit + youtube_explode_dart
                                embedUrl: 'https://i.ytimg.com/vi/$vId/maxresdefault.jpg',
                              ));
                              if (mounted) {
                                Navigator.pop(context);
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (_) => PlayerScreen(
                                      episodes: eps,
                                      currentEpisodeIndex: 0,
                                      movieName: isPlaylist ? 'YouTube Playlist' : 'YouTube Video',
                                      lazyPlaylistUrl: isPlaylist ? url : null,
                                    ),
                                  ),
                                );
                              }
                              return;
                          }
                          
                          Navigator.pop(context);
                          Navigator.push("""
                          
    if old_code in content:
        content = content.replace(old_code, new_code)
        print("Injected YouTube logic into library_screen.dart!")
    else:
        print("Target not found!")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_lib('lib/screens/library_screen.dart')
