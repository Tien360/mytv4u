import os
content = open('lib/screens/library_screen.dart', 'r', encoding='utf-8').read()

old_code = '''                          if (isAudio) {
                            if (context.mounted) {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => AudioPlayerScreen(
                                    files: files.files,
                                    initialIndex: 0,
                                  ),
                                ),
                              );
                            }
                          } else if (files.files.first.path != null) {'''

new_code = '''                          if (isAudio) {
                            var audioFiles = files.files.where((f) {
                              String e = f.name.split('.').last.toLowerCase();
                              return ['mp3', 'm4a', 'wav', 'flac', 'aac', 'ogg', 'wma', 'opus', 'amr'].contains(e);
                            }).toList();
                            if (context.mounted) {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => AudioPlayerScreen(
                                    files: audioFiles,
                                    initialIndex: 0,
                                  ),
                                ),
                              );
                            }
                          } else if (files.files.first.path != null) {'''

content = content.replace(old_code, new_code)
open('lib/screens/library_screen.dart', 'w', encoding='utf-8').write(content)
