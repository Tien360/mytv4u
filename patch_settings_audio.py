import re
import sys

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add state variables
state_vars = """    bool _ambientBg = true;
    String _audioVisualizer = 'bars';
    int _audioSleepTimer = 0;"""
content = re.sub(r'    bool _ambientBg = true;', state_vars, content)

# 2. Add loading settings
load_settings = """          _ambientBg = prefs.getBool('enable_ambient_bg') ?? true;
          _audioVisualizer = prefs.getString('audio_visualizer') ?? 'bars';
          _audioSleepTimer = prefs.getInt('audio_sleep_timer') ?? 0;"""
content = re.sub(r'          _ambientBg = prefs.getBool\(\'enable_ambient_bg\'\) \?\? true;', load_settings, content)

# 3. Add UI elements
ui_elements = """                                          ),
                                      const Divider(color: Colors.white12),
                                      ListTile(
                                        title: const Text('Audio Visualizer', style: TextStyle(color: Colors.white, fontSize: 16)),
                                        subtitle: const Text('Style of the audio visualizer', style: TextStyle(color: Colors.white54, fontSize: 12)),
                                        secondary: const Icon(Icons.graphic_eq, color: Colors.white70),
                                        trailing: DropdownButton<String>(
                                          value: _audioVisualizer,
                                          dropdownColor: Colors.grey[900],
                                          style: const TextStyle(color: Colors.white),
                                          underline: Container(),
                                          items: const [
                                            DropdownMenuItem(value: 'bars', child: Text('Bars')),
                                            DropdownMenuItem(value: 'waves', child: Text('Waves')),
                                            DropdownMenuItem(value: 'none', child: Text('None')),
                                          ],
                                          onChanged: (val) async {
                                            if (val != null) {
                                              final prefs = await SharedPreferences.getInstance();
                                              await prefs.setString('audio_visualizer', val);
                                              setState(() => _audioVisualizer = val);
                                            }
                                          },
                                        ),
                                      ),
                                      const Divider(color: Colors.white12),
                                      ListTile(
                                        title: const Text('Audio Sleep Timer (minutes)', style: TextStyle(color: Colors.white, fontSize: 16)),
                                        subtitle: const Text('0 to disable', style: TextStyle(color: Colors.white54, fontSize: 12)),
                                        secondary: const Icon(Icons.timer, color: Colors.white70),
                                        trailing: DropdownButton<int>(
                                          value: _audioSleepTimer,
                                          dropdownColor: Colors.grey[900],
                                          style: const TextStyle(color: Colors.white),
                                          underline: Container(),
                                          items: [0, 15, 30, 45, 60].map((int value) {
                                            return DropdownMenuItem<int>(
                                              value: value,
                                              child: Text(value == 0 ? 'Off' : '$value min'),
                                            );
                                          }).toList(),
                                          onChanged: (val) async {
                                            if (val != null) {
                                              final prefs = await SharedPreferences.getInstance();
                                              await prefs.setInt('audio_sleep_timer', val);
                                              setState(() => _audioSleepTimer = val);
                                            }
                                          },
                                        ),
                                      ),"""
content = re.sub(r'                                          \),\n                                            const Divider\(color: Colors.white12\),\n                                            SwitchListTile\(\n                                              title: Text\(L10n.t\(\'setting_egg_title\'\)', ui_elements + r'\n                                            const Divider(color: Colors.white12),\n                                            SwitchListTile(\n                                              title: Text(L10n.t(\'setting_egg_title\')', content)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
