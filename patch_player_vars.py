import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_audio = """  Widget _buildAudioBackground() {
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
                image: widget.movie.posterUrl.isNotEmpty
                    ? DecorationImage(
                        image: CachedNetworkImageProvider(widget.movie.posterUrl),
                        fit: BoxFit.cover,
                      )
                    : null,
                color: Colors.grey[900],
              ),
              child: widget.movie.posterUrl.isEmpty
                  ? const Icon(Icons.music_note, size: 80, color: Colors.white54)
                  : null,
            ).animate(
              target: _isPlaying ? 1 : 0,
              onComplete: (controller) {
                if (_isPlaying) controller.repeat();
              }
            ).rotate(duration: 10.seconds, curve: Curves.linear),
            const SizedBox(height: 40),
            Text(
              widget.movie.name,
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.white,
                shadows: [Shadow(color: Colors.black54, blurRadius: 4)],
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              widget.episode.name,
              style: const TextStyle(
                fontSize: 16,
                color: Colors.white70,
              ),
              textAlign: TextAlign.center,
            ),
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
  }"""

good_audio = """  Widget _buildAudioBackground() {
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
  }"""

content = content.replace(bad_audio, good_audio)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched variables in player_screen.dart")
