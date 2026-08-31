import re

def add_lazy(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the Dán link block where we parse Youtube
    old_code = """                              if (isYtLinked && url.contains('v=') && (url.contains('list=') || url.contains('playlist?'))) {
                                try {
                                  final uri = Uri.parse(url);
                                  final v = uri.queryParameters['v'];
                                  if (v != null) {
                                    eps.add(Episode(
                                      name: L10n.t('loading_mix_playlist'),
                                      slug: v,
                                      m3u8Url: 'https://www.youtube.com/watch?v=$v',
                                      embedUrl: 'https://i.ytimg.com/vi/$v/maxresdefault.jpg'
                                    ));
                                    if (mounted) {
                                      Navigator.pop(context); // close dialog
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder: (_) => PlayerScreen(
                                            episodes: eps,
                                            currentEpisodeIndex: 0,
                                            movieName: 'YouTube Mix / Playlist',
                                            lazyPlaylistUrl: url,
                                          ),
                                        ),
                                      );
                                    }
                                  }
                                } catch (e) {
                                  debugPrint('Parse error: $e');
                                }
                                return;
                              }"""
                              
    # We will insert a clean check at the top of the URL checking block
    insert_target = "if (url.startsWith('http')) {"
    
    new_code = """if (url.startsWith('http')) {
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

                              eps.add(Episode(
                                name: isPlaylist ? 'YouTube Playlist' : 'YouTube Video',
                                slug: vId,
                                m3u8Url: 'https://www.youtube.com/watch?v=$vId', // media_kit + youtube_explode_dart
                                embedUrl: 'https://i.ytimg.com/vi/$vId/maxresdefault.jpg',
                              ));
                              if (mounted) {
                                Navigator.pop(context); // close dialog
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
                            }"""
                            
    if insert_target in content:
        content = content.replace(insert_target, new_code)
        print("Added youtube logic back to library_screen.dart!")
    else:
        print("Could not find insert target!")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

add_lazy('lib/screens/library_screen.dart')
