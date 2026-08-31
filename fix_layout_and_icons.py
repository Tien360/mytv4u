import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# Fix 1: The Stack size. Wrap the whole AspectRatio in a Center + SizedBox to constrain its maximum size
old_aspect_ratio = '''                            : AspectRatio(
                                aspectRatio: 1,
                                child: Stack(
                                  alignment: Alignment.center,
                                  children: [
                                    if (visualizerType == 'circle')
                                      Positioned.fill(
                                        child: AudioVisualizer(isPlaying: isPlaying, type: 'circle', radius: 170, color: _dominantColor),
                                      ),
                                    AnimatedBuilder('''
new_aspect_ratio = '''                            : Center(
                                child: Container(
                                  width: 320,
                                  height: 320,
                                  child: Stack(
                                    clipBehavior: Clip.none,
                                    alignment: Alignment.center,
                                    children: [
                                      if (visualizerType == 'circle')
                                        Positioned.fill(
                                          child: AudioVisualizer(isPlaying: isPlaying, type: 'circle', radius: 170, color: _dominantColor),
                                        ),
                                      AnimatedBuilder('''
content = content.replace(old_aspect_ratio, new_aspect_ratio)

# Fix 2: Restore the original assets instead of Icons!
old_podcast = '''                                  child: coverArt == null
                                      ? const Padding(
                                          padding: EdgeInsets.all(48.0),
                                          child: Icon(Icons.mic, size: 80, color: Colors.blueAccent),
                                        )
                                      : null,'''
new_podcast = '''                                  child: coverArt == null
                                      ? Padding(
                                          padding: const EdgeInsets.all(48.0),
                                          child: Image.asset('assets/images/podcast_icon.png', color: Colors.blueAccent),
                                        )
                                      : null,'''
content = content.replace(old_podcast, new_podcast)

# Restore Vinyl fallback image
old_vinyl_box = '''                                          boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 20)],
                                          image: coverArt != null
                                              ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                              : null,
                                        ),
                                        child: Stack('''
new_vinyl_box = '''                                          boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 20)],
                                          image: coverArt != null
                                              ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                              : const DecorationImage(image: AssetImage('assets/images/music_icon.png'), fit: BoxFit.cover),
                                        ),
                                        child: Stack('''
content = content.replace(old_vinyl_box, new_vinyl_box)

old_vinyl_icon = '''                                            if (coverArt == null)
                                              const Icon(Icons.music_note, size: 80, color: Colors.white24),
                                            // Center hole'''
new_vinyl_icon = '''                                            // Center hole'''
content = content.replace(old_vinyl_icon, new_vinyl_icon)

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)

