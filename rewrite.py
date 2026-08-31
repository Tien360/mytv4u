import os
import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()
if "import 'dart:ui';" not in content:
    content = content.replace("import 'dart:math' as math;", "import 'dart:math' as math;\nimport 'dart:ui';")

new_build = '''
  @override
  Widget build(BuildContext context) {
    bool isPodcast = duration.inMinutes >= 30;

    return Scaffold(
      body: Stack(
        children: [
          // Background
          Positioned.fill(
            child: coverArt != null
                ? Image.memory(coverArt!, fit: BoxFit.cover)
                : Container(
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [Color(0xFF2C3E50), Colors.black],
                      ),
                    ),
                  ),
          ),
          // Blur and Gradient Overlay
          Positioned.fill(
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 60.0, sigmaY: 60.0),
              child: Container(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [
                      Colors.black.withOpacity(0.3),
                      Colors.black.withOpacity(0.8),
                      Colors.black,
                    ],
                    stops: const [0.0, 0.5, 1.0],
                  ),
                ),
              ),
            ),
          ),
          // Content
          SafeArea(
            child: Column(
              children: [
                // AppBar
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 8.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.keyboard_arrow_down, color: Colors.white, size: 32),
                        onPressed: () => Navigator.pop(context),
                      ),
                      Text(
                        isPodcast ? L10n.t('podcast') ?? "Podcast" : L10n.t('audio_player_title') ?? "Audio Player",
                        style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600, letterSpacing: 1.0),
                      ),
                      Row(
                        children: [
                          IconButton(
                            icon: const Icon(Icons.settings, color: Colors.white),
                            onPressed: () {
                              Navigator.push(context, MaterialPageRoute(builder: (_) => const SettingsScreen())).then((_) {
                                _loadSettings();
                              });
                            },
                          ),
                          IconButton(
                            icon: const Icon(Icons.queue_music, color: Colors.white),
                            onPressed: () {
                              showModalBottomSheet(
                                context: context,
                                backgroundColor: Colors.transparent,
                                builder: (context) => Container(
                                  decoration: BoxDecoration(
                                    color: Colors.grey[900],
                                    borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
                                  ),
                                  child: Column(
                                    children: [
                                      const SizedBox(height: 12),
                                      Container(width: 40, height: 5, decoration: BoxDecoration(color: Colors.grey[600], borderRadius: BorderRadius.circular(10))),
                                      const SizedBox(height: 16),
                                      Text(L10n.t('playlist') ?? "Danh sách phát", style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                                      const SizedBox(height: 16),
                                      Expanded(
                                        child: ListView.builder(
                                          itemCount: widget.files.length,
                                          itemBuilder: (context, index) {
                                            bool active = index == currentIndex;
                                            return ListTile(
                                              leading: Icon(active ? Icons.volume_up : Icons.music_note, color: active ? Colors.blueAccent : Colors.white54),
                                              title: Text(
                                                widget.files[index].name.replaceAll(RegExp(r'\.[a-zA-Z0-9]+$'), ''),
                                                style: TextStyle(color: active ? Colors.blueAccent : Colors.white, fontWeight: active ? FontWeight.bold : FontWeight.normal),
                                              ),
                                              onTap: () {
                                                Navigator.pop(context);
                                                currentIndex = index;
                                                _loadCurrent();
                                              },
                                            );
                                          }
                                        ),
                                      ),
                                    ],
                                  ),
                                )
                              );
                            },
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 32.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        // Artwork / Vinyl
                        Hero(
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
                                )
                              : AnimatedBuilder(
                                  animation: _spinController,
                                  builder: (_, child) {
                                    return Transform.rotate(
                                      angle: _spinController.value * 2 * math.pi,
                                      child: child,
                                    );
                                  },
                                  child: Container(
                                    width: 320,
                                    height: 320,
                                    decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      color: const Color(0xFF121212),
                                      boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 40, offset: Offset(0, 20))],
                                      border: Border.all(color: Colors.white12, width: 1),
                                    ),
                                    child: Stack(
                                      alignment: Alignment.center,
                                      children: [
                                        // Vinyl grooves
                                        for (double w = 300; w > 120; w -= 20)
                                          Container(
                                            width: w,
                                            height: w,
                                            decoration: BoxDecoration(
                                              shape: BoxShape.circle,
                                              border: Border.all(color: Colors.white.withOpacity(0.03), width: 1.5),
                                            ),
                                          ),
                                        // Center label
                                        Container(
                                          width: 130,
                                          height: 130,
                                          decoration: BoxDecoration(
                                            shape: BoxShape.circle,
                                            image: coverArt != null
                                                ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                                : null,
                                            color: Colors.grey[900],
                                          ),
                                          child: coverArt == null ? const Icon(Icons.music_note, size: 50, color: Colors.white24) : null,
                                        ),
                                        // Spindle hole
                                        Container(
                                          width: 12,
                                          height: 12,
                                          decoration: const BoxDecoration(shape: BoxShape.circle, color: Colors.black),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                        ),
                        
                        const SizedBox(height: 60),
                        
                        // Text Info
                        Align(
                          alignment: Alignment.centerLeft,
                          child: Text(
                            title,
                            style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Align(
                          alignment: Alignment.centerLeft,
                          child: Text(
                            artist,
                            style: TextStyle(fontSize: 18, color: Colors.white.withOpacity(0.7)),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        
                        const SizedBox(height: 16),
                        
                        // Visualizer
                        Align(
                          alignment: Alignment.centerLeft,
                          child: AudioVisualizer(isPlaying: isPlaying, type: visualizerType),
                        ),
                        
                        const SizedBox(height: 24),
                        
                        // Progress Bar
                        SliderTheme(
                          data: SliderThemeData(
                            trackHeight: 4,
                            thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 6),
                            overlayShape: const RoundSliderOverlayShape(overlayRadius: 14),
                            activeTrackColor: Colors.white,
                            inactiveTrackColor: Colors.white.withOpacity(0.2),
                            thumbColor: Colors.white,
                            overlayColor: Colors.white.withOpacity(0.1),
                          ),
                          child: Slider(
                            value: position.inMilliseconds.toDouble(),
                            max: math.max(duration.inMilliseconds.toDouble(), position.inMilliseconds.toDouble() + 1),
                            onChanged: (val) {
                              player.seek(Duration(milliseconds: val.toInt()));
                            },
                          ),
                        ),
                        
                        // Time labels
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 4.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(_formatDuration(position), style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 12)),
                              Text(_formatDuration(duration), style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 12)),
                            ],
                          ),
                        ),
                        
                        const SizedBox(height: 32),
                        
                        // Controls
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          children: [
                            IconButton(
                              icon: Icon(Icons.shuffle, color: isShuffle ? Colors.blueAccent : Colors.white.withOpacity(0.5)),
                              iconSize: 28,
                              onPressed: () => setState(() => isShuffle = !isShuffle),
                            ),
                            IconButton(
                              icon: const Icon(Icons.skip_previous_rounded, color: Colors.white),
                              iconSize: 48,
                              onPressed: _prev,
                            ),
                            Container(
                              width: 80,
                              height: 80,
                              decoration: const BoxDecoration(shape: BoxShape.circle, color: Colors.white),
                              child: IconButton(
                                icon: Icon(isPlaying ? Icons.pause_rounded : Icons.play_arrow_rounded, color: Colors.black),
                                iconSize: 48,
                                onPressed: () {
                                  if (isPlaying) {
                                    player.pause();
                                  } else {
                                    player.play();
                                  }
                                },
                              ),
                            ),
                            IconButton(
                              icon: const Icon(Icons.skip_next_rounded, color: Colors.white),
                              iconSize: 48,
                              onPressed: _next,
                            ),
                            IconButton(
                              icon: Icon(
                                repeatMode == 0 ? Icons.repeat : (repeatMode == 1 ? Icons.repeat : Icons.repeat_one),
                                color: repeatMode != 0 ? Colors.blueAccent : Colors.white.withOpacity(0.5)
                              ),
                              iconSize: 28,
                              onPressed: () {
                                setState(() {
                                  repeatMode = (repeatMode + 1) % 3;
                                });
                              },
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
'''

match = re.search(r'  @override\n  Widget build\(BuildContext context\) \{.*\}\n\}', content, re.DOTALL)
if match:
    content = content.replace(match.group(0), new_build)
else:
    print("Not found")

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
