import re

with open('lib/screens/library_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

header = '''
            Padding(
              padding: const EdgeInsets.only(left: 24, right: 24, top: 24, bottom: 16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    L10n.t('favorite_list') != null && L10n.t('favorite_list').isNotEmpty ? L10n.t('favorite_list') : 'Thư viện & Yêu thích',
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  ElevatedButton.icon(
                    icon: const Icon(Icons.folder_open, color: Colors.white),
                    label: const Text('Mở file trên máy', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white.withOpacity(0.1),
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                    ),
                    onPressed: () async {
                      import_file_picker();
                    },
                  ),
                ],
              ),
            ),
'''

# First, add the imports at the top
if 'package:file_picker/file_picker.dart' not in content:
    content = "import 'package:file_picker/file_picker.dart';\n" + content

# Replace the Padding section
padding_regex = r'Padding\(\s*padding:\s*const EdgeInsets\.only\(left:\s*24,\s*top:\s*24,\s*bottom:\s*16\),\s*child:\s*Text\([\s\S]*?fontWeight:\s*FontWeight\.bold,\s*\),\s*\),\s*\),'
content = re.sub(padding_regex, header, content)

# Now fix the onPressed logic
logic = '''
                      try {
                        FilePickerResult? result = await FilePicker.platform.pickFiles(
                          type: FileType.video,
                        );
                        if (result != null && result.files.single.path != null) {
                          String path = result.files.single.path!;
                          String filename = result.files.single.name;
                          String fileUrl = "file:///" + path.replaceAll(r'\\\\', '/');
                          
                          if (context.mounted) {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => MovieDetailScreen(
                                  slug: 'local_file', // Fake slug
                                  initialMovie: Movie(
                                    name: filename,
                                    originalName: 'Local Video',
                                    slug: 'local_file',
                                    thumbUrl: 'https://via.placeholder.com/400x600.png?text=Local+Video', // Placeholder
                                    posterUrl: '',
                                    currentEpisode: 'Full',
                                    quality: 'HD',
                                    language: 'Local',
                                    year: 'N/A',
                                    time: 'N/A',
                                    description: 'Đang phát video từ máy tính của bạn: ' + path,
                                    genres: [],
                                    countries: [],
                                    directors: [],
                                    casts: [],
                                    source: 'local',
                                    episodes: [
                                      EpisodeServer(
                                        serverName: 'Máy tính',
                                        items: [
                                          Episode(
                                            name: 'Full',
                                            slug: 'full',
                                            m3u8Url: fileUrl,
                                            embedUrl: '',
                                          )
                                        ]
                                      )
                                    ],
                                  ),
                                ),
                              ),
                            );
                          }
                        }
                      } catch (e) {
                         print("File picker error: " + e.toString());
                      }
'''
content = content.replace('import_file_picker();', logic)

with open('lib/screens/library_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated library_screen.dart')
