import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Add variables
for i, line in enumerate(lines):
    if 'late String _currentUrl;' in line:
        lines.insert(i+1, '  bool _backgroundPlayback = false;\n  bool _wasPlayingBeforeMinimize = false;\n  bool _isPiPMode = false;\n  Rect? _prePiPBounds;\n')
        break

# 2. Add methods
for i, line in enumerate(lines):
    if 'void onWindowLeaveFullScreen() {' in line:
        methods = '''  @override
  void onWindowMinimize() async {
    if (!_backgroundPlayback && mounted && _isPlayerInitialized) {
      _wasPlayingBeforeMinimize = player.state.playing;
      if (_wasPlayingBeforeMinimize) {
        await player.pause();
      }
    }
  }

  @override
  void onWindowRestore() async {
    if (!_backgroundPlayback && mounted && _isPlayerInitialized && _wasPlayingBeforeMinimize) {
      await player.play();
    }
  }

  Future<void> _togglePiPMode() async {
    if (_isPiPMode) {
      setState(() => _isPiPMode = false);
      await windowManager.setAlwaysOnTop(false);
      if (_prePiPBounds != null) {
        await windowManager.setBounds(_prePiPBounds!);
      }
    } else {
      _prePiPBounds = await windowManager.getBounds();
      setState(() => _isPiPMode = true);
      await windowManager.setAlwaysOnTop(true);
      await windowManager.setSize(const Size(400, 225));
      await windowManager.setAlignment(Alignment.bottomRight);
    }
  }

'''
        lines.insert(i-1, methods)
        break

# 3. Load background playback setting
for i, line in enumerate(lines):
    if '_playbackSpeed = prefs.getDouble(\'default_speed\') ?? 1.0;' in line:
        lines.insert(i+1, '        _backgroundPlayback = prefs.getBool(\'background_playback\') ?? false;\n')
        break

# 4. Hide CustomTitleBar
for i, line in enumerate(lines):
    if 'if (!_isFullscreen)' in line and 'CustomTitleBar' in ''.join(lines[i:i+10]):
        lines[i] = '                if (!_isFullscreen && !_isPiPMode)\n'
        break

# 5. Hide Episode panel
for i, line in enumerate(lines):
    if '// 3. Episode Selection Panel (Right Sidebar)' in line:
        lines.insert(i+1, '                if (!_isPiPMode)\n')
        break

# 6. PiP Button in Bottom Toolbar
for i, line in enumerate(lines):
    if '// Fullscreen Button' in line and 'icon: Icon(' in lines[i+1]:
        pip_btn = '''                                            // PiP Button
                                            IconButton(
                                              icon: const Icon(Icons.picture_in_picture_alt, color: Colors.white, size: 20),
                                              onPressed: _togglePiPMode,
                                              tooltip: 'Chế độ PiP',
                                            ),
                                            const SizedBox(width: 10),
'''
        lines.insert(i, pip_btn)
        break

# 7. Hide/simplify bottom controls when PiP
for i, line in enumerate(lines):
    if '// YouTube Red Seekbar with Hover Time Tooltip' in line:
        lines.insert(i, '                                  if (!_isPiPMode)\n')
        break

for i, line in enumerate(lines):
    if '// YouTube Button Row' in line:
        lines.insert(i, '''                                  if (_isPiPMode)
                                    Row(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        IconButton(
                                          icon: Icon(
                                            _isPlaying ? Icons.pause : Icons.play_arrow,
                                            color: Colors.white,
                                            size: 40,
                                          ),
                                          onPressed: () => player.playOrPause(),
                                        ),
                                        const SizedBox(width: 20),
                                        IconButton(
                                          icon: const Icon(
                                            Icons.fullscreen,
                                            color: Colors.white,
                                            size: 40,
                                          ),
                                          onPressed: _togglePiPMode,
                                        ),
                                      ],
                                    ),
                                  if (!_isPiPMode)\n''')
        break


with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done!')
