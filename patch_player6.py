import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import_statement = "import '../widgets/glass_container.dart';"
new_import = "import '../widgets/glass_container.dart';\nimport '../widgets/ambient_background.dart';\nimport '../widgets/audio_visualizer.dart';\nimport 'package:flutter_animate/flutter_animate.dart';"
if "audio_visualizer.dart" not in content:
    content = content.replace(import_statement, new_import)

audio_code = """  bool get _isAudioOnly {
    if (widget.episodes.isEmpty) return false;
    final ep = widget.episodes[widget.currentEpisodeIndex];
    
    final url = ep.m3u8Url.toLowerCase();
    final file = (ep.filename ?? '').toLowerCase();
    final name = ep.name.toLowerCase();
    final movName = widget.movieName.toLowerCase();
    
    bool isAudioExt = url.endsWith('.mp3') || url.endsWith('.m4a') || url.endsWith('.flac') || url.endsWith('.wav') ||
                      file.endsWith('.mp3') || file.endsWith('.m4a') || file.endsWith('.flac') || file.endsWith('.wav') ||
                      name.endsWith('.mp3') || name.endsWith('.m4a') || name.endsWith('.flac') || name.endsWith('.wav') ||
                      movName.endsWith('.mp3') || movName.endsWith('.m4a') || movName.endsWith('.flac') || movName.endsWith('.wav');
                      
    if (isAudioExt) return true;

    bool hasRealVideo = _videoTracks.any((t) => t.id != 'auto' && t.id != 'no');
    if (!hasRealVideo && player.state.duration.inSeconds > 0 && (player.state.width == null || player.state.width == 0)) {
      return true;
    }
    
    return false;
  }

  Widget _buildAudioBackground() {
    final epName = widget.episodes.isNotEmpty && widget.currentEpisodeIndex < widget.episodes.length 
                   ? widget.episodes[widget.currentEpisodeIndex].name 
                   : '';
    return Stack(
      fit: StackFit.expand,
      children: [
        const AmbientBackground(),
        Container(color: Colors.black.withOpacity(0.4)),
        Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 200,
              height: 200,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: const Color(0xFF3B82F6).withOpacity(0.5),
                    blurRadius: 30,
                    spreadRadius: 5,
                  ),
                ],
                gradient: const LinearGradient(
                  colors: [Color(0xFF3B82F6), Color(0xFF8B5CF6)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
              ),
              child: const Icon(Icons.music_note, size: 80, color: Colors.white),
            ).animate(
              target: _isPlaying ? 1 : 0,
              onComplete: (controller) {
                if (_isPlaying) controller.repeat();
              }
            ).rotate(duration: 10.seconds, curve: Curves.linear),
            const SizedBox(height: 40),
            Text(
              widget.movieName,
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.white,
                shadows: [Shadow(color: Colors.black54, blurRadius: 4)],
              ),
              textAlign: TextAlign.center,
            ),
            if (epName.isNotEmpty) ...[
              const SizedBox(height: 8),
              Text(
                epName,
                style: const TextStyle(
                  fontSize: 16,
                  color: Colors.white70,
                ),
                textAlign: TextAlign.center,
              ),
            ],
            const SizedBox(height: 40),
            SizedBox(
              height: 100,
              child: AudioVisualizer(
                isPlaying: _isPlaying,
                color: const Color(0xFF3B82F6),
                barCount: 40,
              ),
            ),
          ],
        ),
      ],
    );
  }

"""

content = content.replace("  Widget _buildNextEpisodeOverlay() {", audio_code + "  Widget _buildNextEpisodeOverlay() {")

video_target = """                  else
                    Center(
                      child: Video(
                        controller: controller,
                        controls: NoVideoControls, // Tắt controls mặc định
                        subtitleViewConfiguration: SubtitleViewConfiguration(
                          style: TextStyle(
                            fontSize: _subSize,
                            color: Colors.white,
                            backgroundColor: Colors.black.withOpacity(
                              _subOpacity,
                            ),
                          ),
                        ),
                      ),
                    ),"""

video_replacement = """                  else
                    Center(
                      child: Stack(
                        fit: StackFit.expand,
                        children: [
                          Video(
                            controller: controller,
                            controls: NoVideoControls, // Tắt controls mặc định
                            subtitleViewConfiguration: SubtitleViewConfiguration(
                              style: TextStyle(
                                fontSize: _subSize,
                                color: Colors.white,
                                backgroundColor: Colors.black.withOpacity(
                                  _subOpacity,
                                ),
                              ),
                            ),
                          ),
                          if (_isAudioOnly)
                            Positioned.fill(
                              child: _buildAudioBackground(),
                            ),
                        ],
                      ),
                    ),"""

if video_target in content:
    content = content.replace(video_target, video_replacement)
    print("SUCCESS: Target found and replaced.")
else:
    print("ERROR: Target NOT found.")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

