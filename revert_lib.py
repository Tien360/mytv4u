import re

def revert_lib(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_code = """                                episodes: [
                                  Episode(
                                    name: (url.contains('youtube.com') || url.contains('youtu.be')) ? 'YouTube Video/Playlist' : 'Stream',
                                    slug: 'stream',
                                    m3u8Url: (url.contains('youtube.com') || url.contains('youtu.be')) ? '' : url,
                                    embedUrl: (url.contains('youtube.com') || url.contains('youtu.be')) ? url : '',
                                  ),
                                ],"""
                                
    new_code = """                                episodes: [
                                  Episode(
                                    name: 'Stream',
                                    slug: 'stream',
                                    m3u8Url: url,
                                    embedUrl: '',
                                  ),
                                ],"""
                                
    if old_code in content:
        content = content.replace(old_code, new_code)
        print("Reverted library_screen.dart episode creation!")
    else:
        print("Could not find episode creation block!")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

revert_lib('lib/screens/library_screen.dart')
