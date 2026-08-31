import os

content = open('lib/screens/library_screen.dart', 'r', encoding='utf-8').read()

import_str = "import 'player_screen.dart';"
content = content.replace(import_str, import_str + "\nimport 'audio_player_screen.dart';")

old_picker = '''var files = await FilePicker.pickFiles(
                          type: FileType.custom,
                          allowedExtensions: [
                            
                            'mp4',
                            'mkv',
                            'avi',
                            'flv',
                            'webm',
                            'mov',
                            'ts',
                            'mp3',
                            'm4a',
                            'wav',
                            'flac',
                            'aac',

                          ],
                          allowMultiple: false,
                        );'''

new_picker = '''var files = await FilePicker.platform.pickFiles(
                          type: FileType.custom,
                          allowedExtensions: [
                            'mp4', 'mkv', 'avi', 'flv', 'webm', 'mov', 'ts',
                            'mp3', 'm4a', 'wav', 'flac', 'aac', 'ogg', 'wma', 'opus', 'amr'
                          ],
                          allowMultiple: true,
                        );'''

content = content.replace(old_picker, new_picker)

old_check = '''if (files != null &&
                            files.isNotEmpty &&
                            files.single.path != null) {
                          String path = files.single.path!;
                          String filename = files.single.name;
                          String fileUrl =
                              "file:///" + path.replaceAll(r'\\\\', '/');

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
                                    ),
                                  ],
                                  currentEpisodeIndex: 0,
                                  movieName: filename,
                                ),
                              ),
                            );
                          }
                        }'''

new_check = '''if (files != null && files.files.isNotEmpty) {
                          String ext = files.files.first.name.split('.').last.toLowerCase();
                          bool isAudio = ['mp3', 'm4a', 'wav', 'flac', 'aac', 'ogg', 'wma', 'opus', 'amr'].contains(ext);
                          if (isAudio) {
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
                          } else if (files.files.first.path != null) {
                            String path = files.files.first.path!;
                            String filename = files.files.first.name;
                            String fileUrl = "file:///" + path.replace('\\\\', '/');

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
                                      ),
                                    ],
                                    currentEpisodeIndex: 0,
                                    movieName: filename,
                                  ),
                                ),
                              );
                            }
                          }
                        }'''
content = content.replace(old_check, new_check)
open('lib/screens/library_screen.dart', 'w', encoding='utf-8').write(content)
