import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

old_artwork = '''                  Widget artworkWidget = Hero(
                    tag: 'artwork',
                    child: isPodcast
                        ? AspectRatio(
                            aspectRatio: 1,
                            child: Container(
                              constraints: const BoxConstraints(maxWidth: 320, maxHeight: 320),
                              decoration: BoxDecoration(
                                color: Colors.grey[800],
                                borderRadius: BorderRadius.circular(24),
                                boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 30, offset: Offset(0, 15))],
                              ),
                              child: Padding(
                                padding: const EdgeInsets.all(48.0),
                                child: Image.asset('assets/images/podcast_icon.png', color: Colors.blueAccent),
                              ),
                            ),
                          )
                        : AspectRatio(
                            aspectRatio: 1,
                            child: Stack(
                              alignment: Alignment.center,
                              children: [
                                if (visualizerType == 'circle')
                                  Positioned.fill(
                                    child: AudioVisualizer(isPlaying: isPlaying, type: 'circle', radius: 170, color: _dominantColor),
                                  ),
                                AnimatedBuilder(
                                  animation: _spinController,
                                  builder: (_, child) {
                                    return Transform.rotate(
                                      angle: _spinController.value * 2 * math.pi,
                                      child: child,
                                    );
                                  },
                                  child: Container(
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
                                ),
                                Positioned(
                                  top: 10,
                                  right: 10,
                                  child: TonearmWidget(isPlaying: isPlaying),
                                ),
                              ],
                            ),
                          ),
                  );'''

new_artwork = '''                  Widget artworkWidget = Hero(
                    tag: 'artwork',
                    child: AnimatedSwitcher(
                      duration: const Duration(milliseconds: 600),
                      switchInCurve: Curves.easeOut,
                      switchOutCurve: Curves.easeIn,
                      transitionBuilder: (child, animation) {
                        return FadeTransition(
                          opacity: animation,
                          child: SlideTransition(
                            position: Tween<Offset>(begin: const Offset(0.05, 0), end: Offset.zero).animate(animation),
                            child: child,
                          ),
                        );
                      },
                      child: KeyedSubtree(
                        key: ValueKey(currentIndex),
                        child: (!showVinyl || isPodcast)
                            ? AspectRatio(
                                aspectRatio: 1,
                                child: Container(
                                  constraints: const BoxConstraints(maxWidth: 320, maxHeight: 320),
                                  decoration: BoxDecoration(
                                    color: Colors.grey[800],
                                    borderRadius: BorderRadius.circular(24),
                                    boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 30, offset: Offset(0, 15))],
                                    image: coverArt != null && !isPodcast
                                        ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                        : null,
                                  ),
                                  child: (coverArt == null || isPodcast)
                                      ? Padding(
                                          padding: const EdgeInsets.all(48.0),
                                          child: Image.asset(isPodcast ? 'assets/images/podcast_icon.png' : 'assets/images/music_icon.png', color: Colors.blueAccent),
                                        )
                                      : null,
                                ),
                              )
                            : AspectRatio(
                                aspectRatio: 1,
                                child: Stack(
                                  alignment: Alignment.center,
                                  children: [
                                    if (visualizerType == 'circle')
                                      Positioned.fill(
                                        child: AudioVisualizer(isPlaying: isPlaying, type: 'circle', radius: 170, color: _dominantColor),
                                      ),
                                    AnimatedBuilder(
                                      animation: _spinController,
                                      builder: (_, child) {
                                        return Transform.rotate(
                                          angle: _spinController.value * 2 * math.pi,
                                          child: child,
                                        );
                                      },
                                      child: Container(
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
                                    ),
                                    Positioned(
                                      top: -10,
                                      left: 10,
                                      child: TonearmWidget(isPlaying: isPlaying),
                                    ),
                                  ],
                                ),
                              ),
                      ),
                    ),
                  );'''

content = content.replace(old_artwork, new_artwork)

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
