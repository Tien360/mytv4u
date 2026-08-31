import os
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# Replace old visualizer with AudioVisualizer
old_viz = '''          if (visualizerType == 'bars')
            SizedBox(
              height: 50,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(5, (index) => AnimatedBuilder(
                  animation: _vizController,
                  builder: (context, child) {
                    return Container(
                      margin: const EdgeInsets.symmetric(horizontal: 4),
                      width: 8,
                      height: 10 + math.Random().nextDouble() * 40 * (isPlaying ? 1 : 0),
                      color: Colors.blueAccent,
                    );
                  },
                )),
              )
            )
          else if (visualizerType == 'waves')
            SizedBox(
              height: 50,
              child: AnimatedBuilder(
                animation: _vizController,
                builder: (context, child) {
                  return Icon(Icons.waves, size: 40 + (isPlaying ? math.Random().nextDouble() * 10 : 0), color: Colors.blueAccent);
                },
              )
            ),'''

new_viz = '''          AudioVisualizer(isPlaying: isPlaying, type: visualizerType),'''

content = content.replace(old_viz, new_viz)

if "import 'audio_visualizer.dart';" not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\\nimport 'audio_visualizer.dart';")

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
