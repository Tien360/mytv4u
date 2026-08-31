import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\library_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure dart:convert and dart:io are imported
if "import 'dart:convert';" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'dart:convert';\nimport 'dart:io';")

search_func = """                        try {
                          final yt = YoutubeExplode();
                          List<Episode> eps = [];
                          String movieName = 'Luồng Mạng';"""
end_func = """                          yt.close();"""

new_logic = """                        try {
                          List<Episode> eps = [];
                          String movieName = 'Luồng Mạng';

                          // Try yt-dlp first
                          try {
                            final exeDir = File(Platform.resolvedExecutable).parent.path;
                            File ytExe = File('$exeDir\\\\yt-dlp.exe');
                            if (!ytExe.existsSync()) {
                              ytExe = File('${Directory.current.path}\\\\build\\\\windows\\\\x64\\\\runner\\\\Release\\\\yt-dlp.exe');
                            }
                            
                            if (ytExe.existsSync() || Platform.isWindows) {
                              final exePath = ytExe.existsSync() ? ytExe.path : 'yt-dlp';
                              final res = await Process.run(exePath, ['--dump-json', '--flat-playlist', url]);
                              if (res.exitCode == 0) {
                                final lines = res.stdout.toString().split('\\n').where((l) => l.trim().isNotEmpty).toList();
                                if (lines.length > 1) {
                                  movieName = 'Playlist (${lines.length} videos)';
                                }
                                for (var line in lines) {
                                  final json = jsonDecode(line);
                                  final title = json['title'] ?? 'Video';
                                  final id = json['id'] ?? '';
                                  final watchUrl = json['url'] ?? url;
                                  
                                  if (lines.length == 1 && json['playlist_title'] != null) {
                                     movieName = json['playlist_title'];
                                  }
                                  
                                  eps.add(Episode(
                                    name: title,
                                    slug: id.isNotEmpty ? 'yt_$id' : 'stream_${DateTime.now().millisecondsSinceEpoch}',
                                    m3u8Url: watchUrl,
                                    embedUrl: id.isNotEmpty ? 'https://i.ytimg.com/vi/$id/maxresdefault.jpg' : '',
                                  ));
                                }
                              }
                            }
                          } catch (e) {
                            print('yt-dlp failed: $e');
                          }
                          
                          // Fallback to youtube_explode_dart if yt-dlp fails
                          if (eps.isEmpty) {
                            final yt = YoutubeExplode();
                            if (url.contains('list=')) {
                              try {
                                final playlist = await yt.playlists.get(url);
                                movieName = playlist.title;
                                final videos = await yt.playlists.getVideos(playlist.id).take(100).toList();
                                for (var v in videos) {
                                  eps.add(Episode(
                                    name: v.title,
                                    slug: 'yt_${v.id.value}',
                                    m3u8Url: v.url,
                                    embedUrl: v.thumbnails.highResUrl,
                                  ));
                                }
                              } catch (_) {}
                            }
                            
                            if (eps.isEmpty) {
                              String slug = 'stream_${DateTime.now().millisecondsSinceEpoch}';
                              try {
                                var video = await yt.videos.get(url);
                                movieName = video.title;
                                eps.add(Episode(
                                  name: video.title,
                                  slug: 'yt_${video.id.value}',
                                  m3u8Url: video.url,
                                  embedUrl: video.thumbnails.highResUrl,
                                ));
                              } catch (_) {
                                eps.add(Episode(
                                  name: 'Stream',
                                  slug: slug,
                                  m3u8Url: url,
                                  embedUrl: '',
                                ));
                              }
                            }
                            yt.close();
                          }
"""

start_idx = content.find(search_func)
end_idx = content.find(end_func) + len(end_func)

if start_idx != -1:
    content = content[:start_idx] + new_logic + content[end_idx:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched library_screen.dart")
else:
    print("Could not find search_func")
