import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# 1. Add _coverCache map
if "Map<String, Uint8List?> _coverCache =" not in content:
    content = content.replace("  Uint8List? coverArt;", "  Uint8List? coverArt;\n  final Map<String, Uint8List?> _coverCache = {};")

# 2. Add _getThumbnail method
thumbnail_method = '''
  Future<Uint8List?> _getThumbnail(String path) async {
    if (_coverCache.containsKey(path)) return _coverCache[path];
    try {
      if (path.toLowerCase().endsWith('.mp3')) {
        // Read async to avoid freezing UI
        final bytes = await File(path).readAsBytes();
        final mp3 = MP3Instance(bytes);
        if (mp3.parseTagsSync()) {
          final tags = mp3.getMetaTags();
          if (tags != null && tags['APIC'] != null) {
            _coverCache[path] = base64Decode(tags['APIC']['base64']);
            return _coverCache[path];
          }
        }
      }
    } catch (_) {}
    _coverCache[path] = null;
    return null;
  }
'''
if "_getThumbnail" not in content:
    content = content.replace("  Future<void> _loadCurrent() async {", thumbnail_method + "\n  Future<void> _loadCurrent() async {")


# 3. Update Playlist to use FutureBuilder and new icons
old_listtile = '''                                                      child: ListTile(
                                                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                                                        leading: Container(
                                                          width: 48,
                                                          height: 48,
                                                          decoration: BoxDecoration(
                                                            color: Colors.grey[850],
                                                            borderRadius: BorderRadius.circular(8),
                                                          ),
                                                          child: active
                                                              ? const Icon(Icons.equalizer, color: Colors.blueAccent)
                                                              : const Icon(Icons.music_note, color: Colors.white54),
                                                        ),'''

new_listtile = '''                                                      child: ListTile(
                                                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                                                        leading: FutureBuilder<Uint8List?>(
                                                          future: _getThumbnail(widget.files[index].path!),
                                                          builder: (context, snapshot) {
                                                            Widget inner;
                                                            if (snapshot.hasData && snapshot.data != null) {
                                                              inner = Image.memory(snapshot.data!, fit: BoxFit.cover, width: 48, height: 48);
                                                            } else {
                                                              bool isPod = duration.inMinutes >= 30; // rough guess
                                                              inner = Padding(
                                                                padding: const EdgeInsets.all(8.0),
                                                                child: Image.asset(isPod ? 'assets/images/podcast_icon.png' : 'assets/images/music_icon.png', color: active ? Colors.blueAccent : Colors.white70),
                                                              );
                                                            }
                                                            return Container(
                                                              width: 48,
                                                              height: 48,
                                                              decoration: BoxDecoration(
                                                                color: Colors.grey[850],
                                                                borderRadius: BorderRadius.circular(8),
                                                              ),
                                                              clipBehavior: Clip.antiAlias,
                                                              child: Stack(
                                                                children: [
                                                                  Positioned.fill(child: inner),
                                                                  if (active)
                                                                    Container(
                                                                      color: Colors.black54,
                                                                      child: const Center(child: Icon(Icons.equalizer, color: Colors.blueAccent)),
                                                                    ),
                                                                ]
                                                              ),
                                                            );
                                                          }
                                                        ),'''
content = content.replace(old_listtile, new_listtile)

# 4. Fix Vinyl and Podcast icon fallback in main UI
old_podcast_hero = '''                          Hero(
                            tag: 'artwork',
                            child: isPodcast
                                ? Container(
                                    width: 300,
                                    height: 300,
                                    decoration: BoxDecoration(
                                      color: Colors.grey[800],
                                      borderRadius: BorderRadius.circular(24),
                                      boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 30, offset: Offset(0, 15))],
                                    ),
                                    child: const Icon(Icons.podcasts, size: 120, color: Colors.blueAccent),
                                  )'''
new_podcast_hero = '''                          Expanded(
                            child: Center(
                              child: Hero(
                                tag: 'artwork',
                                child: isPodcast
                                    ? Container(
                                        width: MediaQuery.of(context).size.width * 0.8,
                                        height: MediaQuery.of(context).size.width * 0.8,
                                        constraints: const BoxConstraints(maxWidth: 350, maxHeight: 350),
                                        decoration: BoxDecoration(
                                          color: Colors.grey[850],
                                          borderRadius: BorderRadius.circular(24),
                                          boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 30, offset: Offset(0, 15))],
                                        ),
                                        child: Padding(
                                          padding: const EdgeInsets.all(48.0),
                                          child: Image.asset('assets/images/podcast_icon.png', color: Colors.blueAccent),
                                        ),
                                      )'''
content = content.replace(old_podcast_hero, new_podcast_hero)

# Fix animated builder constraint
old_animated = '''                                : AnimatedBuilder(
                                    animation: _spinController,
                                    builder: (_, child) {
                                      return Transform.rotate(
                                        angle: _spinController.value * 2 * math.pi,
                                        child: child,
                                      );
                                    },
                                    child: Container(
                                      width: 320,
                                      height: 320,'''
new_animated = '''                                  : AnimatedBuilder(
                                      animation: _spinController,
                                      builder: (_, child) {
                                        return Transform.rotate(
                                          angle: _spinController.value * 2 * math.pi,
                                          child: child,
                                        );
                                      },
                                      child: Container(
                                        width: MediaQuery.of(context).size.width * 0.85,
                                        height: MediaQuery.of(context).size.width * 0.85,
                                        constraints: const BoxConstraints(maxWidth: 380, maxHeight: 380),'''
content = content.replace(old_animated, new_animated)

# Fix music_icon fallback in vinyl
old_spindle = '''                                          Container(
                                            width: 16,
                                            height: 16,
                                            decoration: BoxDecoration(
                                              shape: BoxShape.circle,
                                              color: Colors.black,
                                              border: Border.all(color: Colors.white54, width: 1),
                                              boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 4, offset: Offset(0, 2))],
                                            ),
                                          ),
                                          if (coverArt == null)
                                            const Icon(Icons.music_note, size: 80, color: Colors.white24),
                                        ],
                                      ),
                                    ),
                                  ),
                          ),
                          
                          const SizedBox(height: 60),'''
new_spindle = '''                                          Container(
                                            width: 16,
                                            height: 16,
                                            decoration: BoxDecoration(
                                              shape: BoxShape.circle,
                                              color: Colors.black,
                                              border: Border.all(color: Colors.white54, width: 1),
                                              boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 4, offset: Offset(0, 2))],
                                            ),
                                          ),
                                          if (coverArt == null)
                                            Image.asset('assets/images/music_icon.png', width: 80, height: 80, color: Colors.white24),
                                        ],
                                      ),
                                    ),
                                  ),
                              ),
                            ),
                          ),
                          
                          const SizedBox(height: 20),'''
content = content.replace(old_spindle, new_spindle)

# Close the expanded that we added around Hero artwork!
# The Hero widget was originally not wrapped in Expanded, but we wrapped it in Expanded(child: Center(child: Hero(...) )))
# So we must ensure it's closed correctly. The old_spindle replacement has ), ), ), which closes Center and Expanded.

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
