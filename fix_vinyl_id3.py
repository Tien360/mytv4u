import os
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

import_id3 = "import 'package:id3/id3.dart';\\nimport 'dart:convert';\\nimport 'dart:io';\\n"
if "import 'package:id3/id3.dart';" not in content:
    content = content.replace("import 'audio_visualizer.dart';", "import 'audio_visualizer.dart';\\n" + import_id3)

extract_code = '''    setState(() {
      title = file.name.replaceAll(RegExp(r'\\.[a-zA-Z0-9]+$'), '');
      artist = 'Unknown Artist';
      coverArt = null;
    });
    
    // Try to extract ID3 tags
    try {
      if (path.toLowerCase().endsWith('.mp3')) {
        MP3Instance mp3 = MP3Instance(path);
        if (mp3.parseTagsSync()) {
          Map<String, dynamic>? tags = mp3.getMetaTags();
          if (tags != null) {
            setState(() {
              title = tags['Title'] ?? title;
              artist = tags['Artist'] ?? artist;
              if (tags['APIC'] != null && tags['APIC']['base64'] != null) {
                coverArt = base64Decode(tags['APIC']['base64']);
              }
            });
          }
        }
      }
    } catch (e) {
      // Ignore id3 parsing errors
    }'''

old_extract = '''    setState(() {
      title = file.name.replaceAll(RegExp(r'\\.[a-zA-Z0-9]+$'), '');
      artist = 'Unknown Artist';
      coverArt = null;
    });'''

content = content.replace(old_extract, extract_code)

# Add grooves to vinyl disc
vinyl_ui = '''                      child: Container(
                        width: 250,
                        height: 250,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: Colors.grey[900],
                          border: Border.all(color: Colors.white24, width: 2),
                          boxShadow: [
                            BoxShadow(color: Colors.black.withValues(alpha: 0.8), blurRadius: 15, spreadRadius: 5)
                          ],
                        ),
                        child: Stack(
                          alignment: Alignment.center,
                          children: [
                            // Vinyl grooves
                            Container(
                              width: 230,
                              height: 230,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                border: Border.all(color: Colors.white12, width: 1),
                              ),
                            ),
                            Container(
                              width: 210,
                              height: 210,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                border: Border.all(color: Colors.white12, width: 1),
                              ),
                            ),
                            Container(
                              width: 190,
                              height: 190,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                border: Border.all(color: Colors.white12, width: 1),
                              ),
                            ),
                            Container(
                              width: 170,
                              height: 170,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                border: Border.all(color: Colors.white12, width: 1),
                              ),
                            ),
                            // Center label (Cover Art or fallback)
                            Container(
                              width: 100,
                              height: 100,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                image: coverArt != null
                                    ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                    : null,
                                color: Colors.blueAccent.withValues(alpha: 0.2),
                              ),
                              child: coverArt == null ? const Icon(Icons.music_note, size: 40, color: Colors.blueAccent) : null,
                            ),
                            // Spindle hole
                            Container(
                              width: 15,
                              height: 15,
                              decoration: const BoxDecoration(
                                shape: BoxShape.circle,
                                color: Colors.black,
                              ),
                            ),
                          ],
                        ),
                      ),'''

old_vinyl = '''                      child: Container(
                        width: 250,
                        height: 250,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          image: coverArt != null
                              ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                              : null,
                          color: Colors.grey[900],
                          border: Border.all(color: Colors.white24, width: 2),
                        ),
                        child: coverArt == null ? const Icon(Icons.music_note, size: 80, color: Colors.white54) : null,
                      ),'''

content = content.replace(old_vinyl, vinyl_ui)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
