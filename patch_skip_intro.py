import os
content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()

skip_intro_code = '''
                // Skip Intro Button
                if (!widget.isLive &&
                    _duration.inSeconds > 85 &&
                    _position.inSeconds > 0 &&
                    _position.inSeconds < 85 &&
                    !_isUsingWebview)
                  Positioned(
                    bottom: 100,
                    right: 32,
                    child: ElevatedButton.icon(
                      icon: const Icon(Icons.fast_forward, color: Colors.white),
                      label: const Text("Bỏ qua Intro", style: TextStyle(color: Colors.white)),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.black.withOpacity(0.8),
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                          side: const BorderSide(color: Colors.white24, width: 1),
                        ),
                      ),
                      onPressed: () {
                        player.seek(const Duration(seconds: 85));
                      },
                    ),
                  ),
'''

# Find the Next Episode Overlay comment and insert before it
next_overlay_marker = '// Next Episode Overlay (Near End)'
content = content.replace(next_overlay_marker, skip_intro_code + '\\n                ' + next_overlay_marker)

open('lib/screens/player_screen.dart', 'w', encoding='utf-8').write(content)
