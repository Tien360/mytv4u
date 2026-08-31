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

if "_isAudioOnly" not in content:
    content = content.replace("  Widget _buildNextEpisodeOverlay() {", audio_code + "  Widget _buildNextEpisodeOverlay() {")

# Regex replace Video widget
if "if (_isAudioOnly)" not in content:
    pattern = re.compile(
        r"(else\s+Center\(\s+child:\s+)(Video\(\s+controller:\s+controller,\s+controls:\s+NoVideoControls,[^\)]+\),\s*\n\s*\),\s*\n\s*\),\s*\n\s*\),)",
        re.MULTILINE
    )
    
    # Wait, it's easier to just match from `else \s* Center( \s* child: Video(` up to `), \n ), \n ),`?
    # No, that's too brittle. Let's just find the exact `child: Video(` index, then find the matching `)` using a bracket matching function!

    start_idx = content.find("child: Video(")
    if start_idx != -1:
        # Find matching parenthesis for Video(...)
        idx = start_idx + len("child: Video")
        open_parens = 0
        end_idx = -1
        for i in range(idx, len(content)):
            if content[i] == '(':
                open_parens += 1
            elif content[i] == ')':
                open_parens -= 1
                if open_parens == 0:
                    end_idx = i
                    break
        
        if end_idx != -1:
            video_content = content[start_idx:end_idx+1]
            new_video_content = f"child: Stack(\n                      fit: StackFit.expand,\n                      children: [\n                        {video_content},\n                        if (_isAudioOnly)\n                          Positioned.fill(\n                            child: _buildAudioBackground(),\n                          ),\n                      ],\n                    )"
            content = content[:start_idx] + new_video_content + content[end_idx+1:]
            print("SUCCESS: Regex-free bracket matching replacement applied.")
        else:
            print("ERROR: End bracket not found!")
    else:
        print("ERROR: start_idx not found!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

