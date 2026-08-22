import re

with open('lib/screens/library_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''
                      try {
                        FilePickerResult? result = await FilePicker.platform.pickFiles(
                          type: FileType.custom,
                          allowedExtensions: ['mp4', 'mkv', 'avi', 'flv', 'webm', 'mov', 'ts'],
                        );
                        if (result != null && result.files.single.path != null) {
                          String path = result.files.single.path!;
                          String filename = result.files.single.name;
                          String fileUrl = "file:///" + path.replaceAll(r'\\\\', '/');
                          
                          if (context.mounted) {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => PlayerScreen(
                                  episodes: [
                                    Episode(
                                      name: 'Full',
                                      slug: 'full',
                                      m3u8Url: fileUrl,
                                      embedUrl: '',
                                    )
                                  ],
                                  currentEpisodeIndex: 0,
                                  movieName: filename,
                                ),
                              ),
                            );
                          }
                        }
                      } catch (e) {
                         print("File picker error: " + e.toString());
                      }
'''
content = re.sub(r'try\s*\{\s*FilePickerResult\? result = await FilePicker\.platform\.pickFiles\([\s\S]*?catch\s*\(e\)\s*\{\s*print\("File picker error: " \+ e\.toString\(\)\);\s*\}', replacement, content)

with open('lib/screens/library_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated library_screen.dart")
