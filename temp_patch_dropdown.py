import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

sleep_timer_search = """                                              DropdownMenuItem(value: 60, child: const Text('60')),
                                            ],"""
sleep_timer_replace = """                                              DropdownMenuItem(value: 60, child: const Text('60')),
                                              DropdownMenuItem(value: 120, child: const Text('120')),
                                            ],"""
content = content.replace(sleep_timer_search, sleep_timer_replace)
with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

with open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8') as f:
    content2 = f.read()

sleep_timer_search2 = """                                  DropdownMenuItem(value: 60, child: const Text('60', style: TextStyle(color: Colors.white))),
                                ],"""
sleep_timer_replace2 = """                                  DropdownMenuItem(value: 60, child: const Text('60', style: TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 120, child: const Text('120', style: TextStyle(color: Colors.white))),
                                ],"""
content2 = content2.replace(sleep_timer_search2, sleep_timer_replace2)
with open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content2)
print("Fixed Dropdown assertions!")
