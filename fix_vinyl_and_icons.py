import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# Fix podcast icon tint
old_podcast = '''                                  child: coverArt == null
                                      ? Padding(
                                          padding: const EdgeInsets.all(48.0),
                                          child: Image.asset('assets/images/podcast_icon.png', color: Colors.blueAccent),
                                        )
                                      : null,'''
new_podcast = '''                                  child: coverArt == null
                                      ? Padding(
                                          padding: const EdgeInsets.all(48.0),
                                          child: Image.asset('assets/images/podcast_icon.png'),
                                        )
                                      : null,'''
content = content.replace(old_podcast, new_podcast)

# Fix Vinyl layout
old_vinyl_disc = '''                                      child: Container(
                                        constraints: const BoxConstraints(maxWidth: 320, maxHeight: 320),
                                        decoration: BoxDecoration(
                                          shape: BoxShape.circle,
                                          color: const Color(0xFF1A1A1A),
                                          boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 20)],
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
                                      ),'''

new_vinyl_disc = '''                                      child: Container(
                                        width: 320,
                                        height: 320,
                                        decoration: const BoxDecoration(
                                          shape: BoxShape.circle,
                                          color: Color(0xFF111111),
                                          boxShadow: [BoxShadow(color: Colors.black54, blurRadius: 20)],
                                        ),
                                        child: Stack(
                                          alignment: Alignment.center,
                                          children: [
                                            // Grooves (vân đĩa)
                                            Container(width: 300, height: 300, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white10, width: 1))),
                                            Container(width: 270, height: 270, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white10, width: 1))),
                                            Container(width: 240, height: 240, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white10, width: 1))),
                                            Container(width: 210, height: 210, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white10, width: 1))),
                                            Container(width: 180, height: 180, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white10, width: 1))),
                                            Container(width: 150, height: 150, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white10, width: 1))),
                                            // Album Art (Center Label)
                                            Container(
                                              width: 120,
                                              height: 120,
                                              decoration: BoxDecoration(
                                                shape: BoxShape.circle,
                                                image: coverArt != null
                                                    ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                                    : null,
                                              ),
                                              child: coverArt == null
                                                  ? Padding(
                                                      padding: const EdgeInsets.all(24.0),
                                                      child: Image.asset('assets/images/music_icon.png'),
                                                    )
                                                  : null,
                                            ),
                                            // Center hole
                                            Container(
                                              width: 16,
                                              height: 16,
                                              decoration: BoxDecoration(
                                                shape: BoxShape.circle,
                                                color: Colors.grey[850],
                                                border: Border.all(color: Colors.black, width: 2),
                                              ),
                                            ),
                                            Container(
                                              width: 6,
                                              height: 6,
                                              decoration: const BoxDecoration(
                                                shape: BoxShape.circle,
                                                color: Colors.black87,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),'''

content = content.replace(old_vinyl_disc, new_vinyl_disc)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)

