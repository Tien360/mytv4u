import re

def fix_single_yt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the single youtube video block
    start_str = "else if (url.contains('youtube.com/watch') || url.contains('youtu.be/')) {"
    end_str = "return;\n                              }"
    
    start_idx = content.find(start_str)
    
    # We want the FIRST return; after start_str
    if start_idx != -1:
        end_idx = content.find("return;", start_idx)
        if end_idx != -1:
            end_idx = content.find("}", end_idx) + 1
            
            new_block = '''else if (url.contains('youtube.com/watch') || url.contains('youtu.be/')) {
                                eps.add(Episode(
                                  name: 'YouTube Video',
                                  slug: url,
                                  m3u8Url: '', // Force Webview to bypass yt-dlp anti-bot issues
                                  embedUrl: url,
                                ));
                                if (mounted) {
                                  Navigator.pop(context); // close dialog
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (_) => PlayerScreen(
                                        episodes: eps,
                                        currentEpisodeIndex: 0,
                                        movieName: 'YouTube Video',
                                      ),
                                    ),
                                  );
                                }
                                return;
                              }'''
            
            content = content[:start_idx] + new_block + content[end_idx:]
            print("Patched single youtube in library_screen.dart!")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_single_yt('lib/screens/library_screen.dart')
