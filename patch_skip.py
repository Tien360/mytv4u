import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add state variables
if "bool _enableSkipIntro" not in content:
    content = content.replace("bool _autoNext = true;", "bool _autoNext = true;\n  bool _enableSkipIntro = true;\n  int _skipIntroDuration = 85;")

# 2. Add load logic
old_load = """      if (mounted) {
        setState(() {
          _hwAccel = prefs.getBool('enable_hw_accel') ?? true;
          _subSize = prefs.getDouble('sub_size') ?? 24.0;
          _subOpacity = prefs.getDouble('sub_opacity') ?? 0.3;
        });
      }"""
new_load = """      if (mounted) {
        setState(() {
          _hwAccel = prefs.getBool('enable_hw_accel') ?? true;
          _subSize = prefs.getDouble('sub_size') ?? 24.0;
          _subOpacity = prefs.getDouble('sub_opacity') ?? 0.3;
          _enableSkipIntro = prefs.getBool('enable_skip_intro') ?? true;
          _skipIntroDuration = prefs.getInt('skip_intro_duration') ?? 85;
          _autoNext = prefs.getBool('auto_next') ?? true;
        });
      }"""
content = content.replace(old_load, new_load)

# 3. Add overlay
old_overlay = """                // 2. Controls Layer
                AnimatedOpacity("""
new_overlay = """                // Skip Intro Overlay
                if (_enableSkipIntro && _position.inSeconds > 0 && _position.inSeconds < 180 && _showControls && !_isLiveStream && !_isYoutube)
                  Positioned(
                    bottom: 110,
                    right: 32,
                    child: TweenAnimationBuilder<double>(
                      tween: Tween(begin: 0.0, end: 1.0),
                      duration: const Duration(milliseconds: 300),
                      builder: (context, val, child) {
                        return Opacity(
                          opacity: val,
                          child: Transform.translate(
                            offset: Offset(20 * (1 - val), 0),
                            child: child,
                          ),
                        );
                      },
                      child: OutlinedButton.icon(
                        style: OutlinedButton.styleFrom(
                          backgroundColor: Colors.black.withOpacity(0.5),
                          foregroundColor: Colors.white,
                          side: const BorderSide(color: Colors.white70),
                          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                        ),
                        icon: const Icon(Icons.fast_forward),
                        label: const Text('Bỏ qua Intro', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                        onPressed: () {
                          player.seek(Duration(seconds: _position.inSeconds + _skipIntroDuration));
                        },
                      ),
                    ),
                  ),

                // 2. Controls Layer
                AnimatedOpacity("""
content = content.replace(old_overlay, new_overlay)

# 4. Add UI in General Tab
old_ui = """                                const Divider(color: Colors.white24),

                                ListTile(
                                  leading: Icon(Icons.timer, color: _sleepSecondsRemaining > 0 ? Colors.blueAccent : Colors.white),"""
new_ui = """                                const Divider(color: Colors.white24),
                                
                                SwitchListTile(
                                  secondary: const Icon(Icons.fast_forward, color: Colors.blueAccent),
                                  title: const Text('Tự động bỏ qua Intro', style: TextStyle(color: Colors.white)),
                                  value: _enableSkipIntro,
                                  onChanged: (val) async {
                                    setState(() => _enableSkipIntro = val);
                                    setTabState(() {});
                                    final prefs = await SharedPreferences.getInstance();
                                    await prefs.setBool('enable_skip_intro', val);
                                  },
                                ),
                                if (_enableSkipIntro) ...[
                                  ListTile(
                                    title: const Text('Thời gian bỏ qua', style: TextStyle(color: Colors.white70)),
                                    trailing: SizedBox(
                                      width: 160,
                                      child: Row(
                                        mainAxisAlignment: MainAxisAlignment.end,
                                        children: [
                                          Text('$_skipIntroDuration s', style: const TextStyle(color: Colors.white70)),
                                          Expanded(
                                            child: Slider(
                                              value: _skipIntroDuration.toDouble(),
                                              min: 30,
                                              max: 180,
                                              divisions: 30,
                                              onChanged: (val) async {
                                                setState(() => _skipIntroDuration = val.toInt());
                                                setTabState(() {});
                                                final prefs = await SharedPreferences.getInstance();
                                                await prefs.setInt('skip_intro_duration', val.toInt());
                                              },
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                ],
                                const Divider(color: Colors.white24),

                                ListTile(
                                  leading: Icon(Icons.timer, color: _sleepSecondsRemaining > 0 ? Colors.blueAccent : Colors.white),"""
content = content.replace(old_ui, new_ui)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated player_screen skip intro logic")
