import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# 1. Update text alignment and overflow
old_text = '''                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      title,
                                      style: const TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold),
                                    ),
                                    const SizedBox(height: 8),
                                    Text(
                                      artist,
                                      style: const TextStyle(color: Colors.white70, fontSize: 20),
                                    ),'''

new_text = '''                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    Text(
                                      title,
                                      textAlign: TextAlign.center,
                                      maxLines: 2,
                                      overflow: TextOverflow.ellipsis,
                                      style: const TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold),
                                    ),
                                    const SizedBox(height: 8),
                                    Text(
                                      artist,
                                      textAlign: TextAlign.center,
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                      style: const TextStyle(color: Colors.white70, fontSize: 20),
                                    ),'''

content = content.replace(old_text, new_text)

# Also update the portrait layout text alignment
old_text_portrait = '''                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      title,
                                      style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      artist,
                                      style: const TextStyle(color: Colors.white70, fontSize: 16),
                                    ),'''

new_text_portrait = '''                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    Text(
                                      title,
                                      textAlign: TextAlign.center,
                                      maxLines: 2,
                                      overflow: TextOverflow.ellipsis,
                                      style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      artist,
                                      textAlign: TextAlign.center,
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                      style: const TextStyle(color: Colors.white70, fontSize: 16),
                                    ),'''

content = content.replace(old_text_portrait, new_text_portrait)


# 2. Update Vinyl Layout (full coverArt + grooves on top)
old_vinyl = '''                                      child: Container(
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

new_vinyl = '''                                      child: Container(
                                        width: 320,
                                        height: 320,
                                        decoration: BoxDecoration(
                                          shape: BoxShape.circle,
                                          color: const Color(0xFF111111),
                                          boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 20)],
                                          image: coverArt != null
                                              ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                              : null,
                                        ),
                                        child: Stack(
                                          alignment: Alignment.center,
                                          children: [
                                            if (coverArt == null)
                                              Padding(
                                                padding: const EdgeInsets.all(80.0),
                                                child: Image.asset('assets/images/music_icon.png'),
                                              ),
                                            // Semi-transparent overlay to make grooves visible over bright images
                                            if (coverArt != null)
                                              Container(
                                                decoration: const BoxDecoration(
                                                  shape: BoxShape.circle,
                                                  color: Colors.black12,
                                                ),
                                              ),
                                            // Grooves (vân đĩa) over the image
                                            Container(width: 300, height: 300, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 270, height: 270, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 240, height: 240, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 210, height: 210, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 180, height: 180, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 150, height: 150, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 120, height: 120, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 90, height: 90, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 60, height: 60, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            
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

content = content.replace(old_vinyl, new_vinyl)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)

