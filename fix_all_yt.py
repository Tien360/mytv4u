import re

def rewrite_yt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the block where youtube urls are processed in library_screen.dart
    # Around line 390
    
    start_str = "if (isYtLinked && url.contains('v=') && (url.contains('list=') || url.contains('playlist?'))) {"
    end_str = "return;\n                              }"
    
    start_idx = content.find(start_str)
    
    if start_idx != -1:
        # We need to find the SECOND return; because there's one for playlist and one for single video!
        # Actually let's just find the exact block for single video too:
        
        single_yt_start = "else if (url.contains('youtube.com/watch') || url.contains('youtu.be/')) {"
        single_yt_idx = content.find(single_yt_start, start_idx)
        
        single_end_idx = content.find("return;", single_yt_idx) + len("return;")
        
        # Replace the entire chunk from start_idx to single_end_idx + 32 (to include closing brace)
        # We will just write a custom block that handles BOTH:
        
        # We want to replace everything from start_str up to the end of the single youtube block
        
        chunk = content[start_idx:single_end_idx + 50]
        actual_end_idx = single_end_idx + chunk[single_end_idx:].find("}") + 1
        
        new_block = '''if (url.contains('youtube.com') || url.contains('youtu.be')) {
                                try {
                                  final uri = Uri.parse(url);
                                  final v = uri.queryParameters['v'] ?? '';
                                  eps.add(Episode(
                                    name: (url.contains('list=') || url.contains('playlist?')) 
                                        ? (L10n.t('youtube_playlist') ?? 'YouTube Playlist') 
                                        : 'YouTube Video',
                                    slug: v.isNotEmpty ? v : url,
                                    m3u8Url: '', // FORCE Webview (bypasses media_kit / yt-dlp anti-bot block)
                                    embedUrl: url, // tv_web_player.exe will natively render this URL!
                                  ));
                                  if (mounted) {
                                    Navigator.pop(context); // close dialog
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (_) => PlayerScreen(
                                          episodes: eps,
                                          currentEpisodeIndex: 0,
                                          movieName: (url.contains('list=') || url.contains('playlist?')) 
                                              ? 'YouTube Playlist' : 'YouTube Video',
                                          lazyPlaylistUrl: null, // DO NOT trigger yt-dlp lazy load!
                                        ),
                                      ),
                                    );
                                  }
                                } catch (e) {
                                  debugPrint('Parse error: $e');
                                }
                                return;
                              }'''
        
        content = content[:start_idx] + new_block + content[actual_end_idx:]
        print("Patched library_screen.dart for ALL YouTube URLs!")
    else:
        print("Could not find start_str!")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

rewrite_yt('lib/screens/library_screen.dart')
