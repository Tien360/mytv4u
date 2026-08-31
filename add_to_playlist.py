import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# 1. Add _addFiles()
add_files_method = '''  Future<void> _addFiles(Function setSheetState) async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['mp3', 'wav', 'flac', 'm4a', 'aac', 'wma', 'ogg'],
      allowMultiple: true,
    );
    if (result != null && result.files.isNotEmpty) {
      setState(() {
        for (var file in result.files) {
          if (file.path != null) {
            _playlistFiles.add(file);
          }
        }
      });
      setSheetState(() {});
    }
  }
'''
if "_addFiles" not in content:
    content = content.replace("  void _next() {", add_files_method + "\n  void _next() {")

# 2. Update Playlist Title with Add button, wrap in StatefulBuilder
old_playlist = '''                                    child: ClipRRect(
                                      borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
                                      child: BackdropFilter(
                                        filter: ImageFilter.blur(sigmaX: 30, sigmaY: 30),
                                        child: Container(
                                          decoration: BoxDecoration(
                                            color: Colors.black.withOpacity(0.6),
                                            border: Border(top: BorderSide(color: Colors.white.withOpacity(0.2))),
                                          ),
                                          child: Column(
                                            children: [
                                              const SizedBox(height: 12),
                                              Container(width: 40, height: 5, decoration: BoxDecoration(color: Colors.white38, borderRadius: BorderRadius.circular(10))),
                                              const SizedBox(height: 16),
                                              Text(L10n.t('playlist') ?? "Danh sách phát", style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold, letterSpacing: 1.2)),
                                              const SizedBox(height: 16),
                                              Expanded(
                                                child: ListView.builder(
                                                  itemCount: _playlistFiles.length,
                                                  itemBuilder: (context, index) {'''

new_playlist = '''                                    child: ClipRRect(
                                      borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
                                      child: BackdropFilter(
                                        filter: ImageFilter.blur(sigmaX: 30, sigmaY: 30),
                                        child: Container(
                                          decoration: BoxDecoration(
                                            color: Colors.black.withOpacity(0.6),
                                            border: Border(top: BorderSide(color: Colors.white.withOpacity(0.2))),
                                          ),
                                          child: StatefulBuilder(
                                            builder: (context, setSheetState) {
                                              return Column(
                                                children: [
                                                  const SizedBox(height: 12),
                                                  Container(width: 40, height: 5, decoration: BoxDecoration(color: Colors.white38, borderRadius: BorderRadius.circular(10))),
                                                  const SizedBox(height: 16),
                                                  Padding(
                                                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                                                    child: Row(
                                                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                                      children: [
                                                        const SizedBox(width: 48), // balance
                                                        Text(L10n.t('playlist') ?? "Danh sách phát", style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold, letterSpacing: 1.2)),
                                                        IconButton(
                                                          icon: const Icon(Icons.add_circle, color: Colors.blueAccent, size: 28),
                                                          onPressed: () => _addFiles(setSheetState),
                                                        ),
                                                      ],
                                                    ),
                                                  ),
                                                  const SizedBox(height: 16),
                                                  Expanded(
                                                    child: ListView.builder(
                                                      itemCount: _playlistFiles.length,
                                                      itemBuilder: (context, index) {'''
content = content.replace(old_playlist, new_playlist)

# 3. Update active icon to use AudioVisualizer(inline)
old_active_icon = '''                                                                  if (active)
                                                                    Container(
                                                                      color: Colors.black54,
                                                                      child: const Center(child: Icon(Icons.equalizer, color: Colors.blueAccent)),
                                                                    ),'''
new_active_icon = '''                                                                  if (active)
                                                                    Container(
                                                                      color: Colors.black54,
                                                                      child: Center(
                                                                        child: AudioVisualizer(
                                                                          isPlaying: isPlaying, 
                                                                          type: 'inline',
                                                                        )
                                                                      ),
                                                                    ),'''
content = content.replace(old_active_icon, new_active_icon)

# Fix missing closing brace for StatefulBuilder we just added
old_close = '''                                                      ),
                                                    );
                                                  }
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ),'''
new_close = '''                                                      ),
                                                    );
                                                  }
                                                ),
                                              ),
                                            ],
                                          );
                                        }
                                      ),
                                    ),
                                  ),'''
content = content.replace(old_close, new_close)

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
