import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# Replace the Stack children for Vinyl to include circle visualizer
old_stack = '''                                      child: Stack(
                                        alignment: Alignment.center,
                                        children: [
                                          if (coverArt != null)
                                            Container(
                                              decoration: BoxDecoration(
                                                shape: BoxShape.circle,
                                                color: Colors.black.withOpacity(0.2),
                                              ),
                                            ),'''
new_stack = '''                                      child: Stack(
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
                                            ),'''
content = content.replace(old_stack, new_stack)

# Replace the text/info area to handle 'bars' and 'inline'
old_info = '''                      Widget infoWidget = Column(
                        crossAxisAlignment: isLandscape ? CrossAxisAlignment.start : CrossAxisAlignment.center,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Align(
                            alignment: isLandscape ? Alignment.centerLeft : Alignment.center,
                            child: Text(
                              title,
                              style: TextStyle(fontSize: isLandscape ? 32 : 24, fontWeight: FontWeight.bold, color: Colors.white),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              textAlign: isLandscape ? TextAlign.left : TextAlign.center,
                            ),
                          ),
                          const SizedBox(height: 6),
                          Row(
                            mainAxisAlignment: isLandscape ? MainAxisAlignment.start : MainAxisAlignment.center,
                            children: [
                              Flexible(
                                child: Text(
                                  artist,
                                  style: TextStyle(fontSize: isLandscape ? 20 : 16, color: Colors.white.withOpacity(0.7)),
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                              const SizedBox(width: 16),
                              AudioVisualizer(isPlaying: isPlaying, type: visualizerType),
                            ],
                          ),
                        ],
                      );'''

new_info = '''                      Widget infoWidget = Column(
                        crossAxisAlignment: isLandscape ? CrossAxisAlignment.start : CrossAxisAlignment.center,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Align(
                            alignment: isLandscape ? Alignment.centerLeft : Alignment.center,
                            child: Text(
                              title,
                              style: TextStyle(fontSize: isLandscape ? 32 : 24, fontWeight: FontWeight.bold, color: Colors.white),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              textAlign: isLandscape ? TextAlign.left : TextAlign.center,
                            ),
                          ),
                          const SizedBox(height: 6),
                          Row(
                            mainAxisAlignment: isLandscape ? MainAxisAlignment.start : MainAxisAlignment.center,
                            children: [
                              Flexible(
                                child: Text(
                                  artist,
                                  style: TextStyle(fontSize: isLandscape ? 20 : 16, color: Colors.white.withOpacity(0.7)),
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                              if (visualizerType == 'inline') ...[
                                const SizedBox(width: 16),
                                AudioVisualizer(isPlaying: isPlaying, type: 'inline'),
                              ]
                            ],
                          ),
                          if (visualizerType == 'bars') ...[
                            const SizedBox(height: 16),
                            AudioVisualizer(isPlaying: isPlaying, type: 'bars'),
                          ]
                        ],
                      );'''

content = content.replace(old_info, new_info)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
