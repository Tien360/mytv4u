import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# Change duration
content = content.replace("duration: const Duration(seconds: 10)", "duration: const Duration(seconds: 3)")

# Fix Visualizer Position and Vinyl size
old_vinyl = '''                                child: AspectRatio(
                                  aspectRatio: 1,
                                  child: Container(
                                    constraints: const BoxConstraints(maxWidth: 450, maxHeight: 450),
                                    decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      color: const Color(0xFF1A1A1A),
                                      image: coverArt != null
                                          ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                          : const DecorationImage(image: AssetImage('assets/images/music_icon.png'), fit: BoxFit.cover),
                                    ),
                                    child: Stack(
                                      alignment: Alignment.center,
                                      children: [
                                        if (visualizerType == 'circle')
                                          Positioned.fill(
                                            child: AudioVisualizer(isPlaying: isPlaying, type: 'circle', radius: 180),
                                          ),
                                        if (coverArt != null)
                                          Container(
                                            decoration: BoxDecoration(
                                              shape: BoxShape.circle,
                                              color: Colors.black.withOpacity(0.2),
                                            ),
                                          ),
                                        // Center hole
                                        Container(
                                          width: 40,
                                          height: 40,
                                          decoration: BoxDecoration(
                                            shape: BoxShape.circle,
                                            color: const Color(0xFF1A1A1A),
                                            border: Border.all(color: Colors.black54, width: 2),
                                          ),
                                        ),
                                        Container(
                                          width: 10,
                                          height: 10,
                                          decoration: const BoxDecoration(
                                            shape: BoxShape.circle,
                                            color: Colors.white24,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),'''
new_vinyl = '''                                child: AspectRatio(
                                  aspectRatio: 1,
                                  child: Stack(
                                    alignment: Alignment.center,
                                    children: [
                                      if (visualizerType == 'circle')
                                        Positioned.fill(
                                          child: AudioVisualizer(isPlaying: isPlaying, type: 'circle', radius: 170, color: _dominantColor),
                                        ),
                                      Container(
                                        constraints: const BoxConstraints(maxWidth: 320, maxHeight: 320),
                                        decoration: BoxDecoration(
                                          shape: BoxShape.circle,
                                          color: const Color(0xFF1A1A1A),
                                          image: coverArt != null
                                              ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                              : const DecorationImage(image: AssetImage('assets/images/music_icon.png'), fit: BoxFit.cover),
                                        ),
                                        child: Stack(
                                          alignment: Alignment.center,
                                          children: [
                                            if (coverArt != null)
                                              Container(
                                                decoration: BoxDecoration(
                                                  shape: BoxShape.circle,
                                                  color: Colors.black.withOpacity(0.2),
                                                ),
                                              ),
                                            // Center hole
                                            Container(
                                              width: 40,
                                              height: 40,
                                              decoration: BoxDecoration(
                                                shape: BoxShape.circle,
                                                color: const Color(0xFF1A1A1A),
                                                border: Border.all(color: Colors.black54, width: 2),
                                              ),
                                            ),
                                            Container(
                                              width: 10,
                                              height: 10,
                                              decoration: const BoxDecoration(
                                                shape: BoxShape.circle,
                                                color: Colors.white24,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                    ],
                                  ),
                                ),'''

content = content.replace(old_vinyl, new_vinyl)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
