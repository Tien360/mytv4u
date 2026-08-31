import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

if 'tonearm_widget.dart' not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport '../widgets/tonearm_widget.dart';")

old_vinyl = '''                                            Container(
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
                                    ],'''

new_vinyl = '''                                            Container(
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
                                      Positioned(
                                        top: 10,
                                        right: 10,
                                        child: TonearmWidget(isPlaying: isPlaying),
                                      ),
                                    ],'''
content = content.replace(old_vinyl, new_vinyl)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
