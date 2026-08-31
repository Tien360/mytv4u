import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

new_methods = '''  Future<Uint8List?> _getCoverForFile(String path) async {
    if (_coverCache.containsKey(path)) return _coverCache[path];
    try {
      if (path.toLowerCase().endsWith('.mp3')) {
        MP3Instance mp3 = MP3Instance(File(path).readAsBytesSync());
        if (mp3.parseTagsSync()) {
          Map<String, dynamic>? tags = mp3.getMetaTags();
          if (tags != null && tags['APIC'] != null && tags['APIC']['base64'] != null) {
            Uint8List bytes = base64Decode(tags['APIC']['base64']);
            _coverCache[path] = bytes;
            return bytes;
          }
        }
      }
    } catch (e) {
      // Ignore
    }
    return null;
  }

  Widget _buildPlaylistPanel() {
    return AnimatedPositioned(
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
      top: 0, bottom: 0,
      right: _showPlaylist ? 0 : -350,
      width: 350,
      child: Material(
        color: Colors.transparent,
        child: Container(
          decoration: BoxDecoration(
            color: Colors.black.withOpacity(0.85),
            border: const Border(left: BorderSide(color: Colors.white24, width: 1)),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(L10n.t('playlist') ?? "Danh sách phát", style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                  Row(
                    children: [
                      IconButton(
                        icon: const Icon(Icons.add_circle_outline, color: Colors.blueAccent),
                        onPressed: () => _addFiles((fn) => setState(fn as void Function())),
                        tooltip: L10n.t('add_to_playlist') ?? 'Thêm nhạc',
                      ),
                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.white54),
                        onPressed: () => setState(() => _showPlaylist = false),
                      ),
                    ],
                  ),
                ],
              ),
              const Divider(color: Colors.white24, height: 32),
              Expanded(
                child: ListView.builder(
                  itemCount: _playlistFiles.length,
                  itemBuilder: (context, i) {
                    final isCurrent = i == currentIndex;
                    return InkWell(
                      onTap: () {
                        setState(() {
                          currentIndex = i;
                          _initPlayer();
                        });
                      },
                      child: Container(
                        padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 8),
                        decoration: BoxDecoration(
                          color: isCurrent ? Colors.blueAccent.withOpacity(0.2) : Colors.transparent,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Row(
                          children: [
                            Container(
                              width: 48,
                              height: 48,
                              decoration: BoxDecoration(
                                color: Colors.white10,
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: isCurrent
                                  ? AudioVisualizer(type: 'inline', color: _dominantColor)
                                  : FutureBuilder<Uint8List?>(
                                      future: _getCoverForFile(_playlistFiles[i].path!),
                                      builder: (context, snapshot) {
                                        if (snapshot.hasData && snapshot.data != null) {
                                          return ClipRRect(
                                            borderRadius: BorderRadius.circular(8),
                                            child: Image.memory(snapshot.data!, fit: BoxFit.cover),
                                          );
                                        }
                                        return const Icon(Icons.music_note, color: Colors.white54);
                                      },
                                    ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Text(
                                _playlistFiles[i].name,
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: TextStyle(
                                  color: isCurrent ? Colors.blueAccent : Colors.white,
                                  fontWeight: isCurrent ? FontWeight.bold : FontWeight.normal,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {'''

content = content.replace('  @override\n  Widget build(BuildContext context) {', new_methods)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
