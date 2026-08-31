import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

skip_ui = """                                          const Divider(color: Colors.white12),
                                          SwitchListTile(
                                            contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                            title: Text(L10n.t('skip_intro') ?? 'Bỏ qua Intro tự động', style: const TextStyle(color: Colors.white)),
                                            value: _prefs?.getBool('enable_skip_intro') ?? true,
                                            activeColor: Colors.blueAccent,
                                            onChanged: (val) async {
                                              setState(() {
                                                _prefs?.setBool('enable_skip_intro', val);
                                              });
                                              _syncToFirebase();
                                            },
                                          ),
                                          if (_prefs?.getBool('enable_skip_intro') ?? true) ...[
                                            ListTile(
                                              contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                                              title: Text(L10n.t('skip_intro_duration') ?? 'Thời lượng bỏ qua', style: const TextStyle(color: Colors.white)),
                                              trailing: SizedBox(
                                                width: 150,
                                                child: Row(
                                                  children: [
                                                    Expanded(
                                                      child: Slider(
                                                        value: (_prefs?.getInt('skip_intro_duration') ?? 85).toDouble(),
                                                        min: 10,
                                                        max: 180,
                                                        divisions: 34,
                                                        activeColor: Colors.blueAccent,
                                                        onChanged: (val) async {
                                                          setState(() {
                                                            _prefs?.setInt('skip_intro_duration', val.toInt());
                                                          });
                                                          _syncToFirebase();
                                                        },
                                                      ),
                                                    ),
                                                    Text('${_prefs?.getInt('skip_intro_duration') ?? 85}s', style: const TextStyle(color: Colors.amber)),
                                                  ],
                                                ),
                                              ),
                                            ),
                                          ],"""

if 'enable_skip_intro' not in content:
    content = content.replace("await prefs.setDouble('default_speed', val);\n                                                }\n                                              },\n                                            ),\n                                          ),", "await prefs.setDouble('default_speed', val);\n                                                }\n                                              },\n                                            ),\n                                          ),\n" + skip_ui)

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
print("Patched settings skip intro!")
