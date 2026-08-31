import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

old_close = '''                                  ],
                                ),
                              ),
                      ),
                    ),
                  );'''

new_close = '''                                  ],
                                ),
                              ),
                            ),
                      ),
                    ),
                  );'''

content = content.replace(old_close, new_close)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
