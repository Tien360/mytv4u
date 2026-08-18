import 'dart:io';

void main() {
  final file = File('lib/screens/player_screen.dart');
  var content = file.readAsStringSync();

  // 1. Add variables
  content = content.replaceFirst('late String _currentUrl;', 'late String _currentUrl;\n  bool _backgroundPlayback = false;\n  bool _wasPlayingBeforeMinimize = false;\n  bool _isPiPMode = false;\n  Rect? _prePiPBounds;');

  // 2. Add methods
  content = content.replaceFirst('void onWindowLeaveFullScreen() {', '''void onWindowLeaveFullScreen() {
    if (mounted) setState(() => _isFullscreen = false);
  }

  @override
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

  void onWindowLeaveFullScreen_placeholder() {''');
  content = content.replaceFirst('void onWindowLeaveFullScreen_placeholder() {\n    if (mounted) setState(() => _isFullscreen = false);\n  }', '');

  // 3. Load setting
  content = content.replaceFirst('_playbackSpeed = prefs.getDouble(\'default_speed\') ?? 1.0;', '_playbackSpeed = prefs.getDouble(\'default_speed\') ?? 1.0;\n        _backgroundPlayback = prefs.getBool(\'background_playback\') ?? false;');

  // 4. Hide CustomTitleBar
  content = content.replaceFirst('if (!_isFullscreen)\n                  const Positioned(\n                    top: 0,\n                    left: 0,\n                    right: 0,\n                    height: 36,\n                    child: CustomTitleBar(),\n                  ),', 'if (!_isFullscreen && !_isPiPMode)\n                  const Positioned(\n                    top: 0,\n                    left: 0,\n                    right: 0,\n                    height: 36,\n                    child: CustomTitleBar(),\n                  ),');

  // 5. Hide Episode panel
  content = content.replaceFirst('AnimatedPositioned(\n                  duration: const Duration(milliseconds: 300),\n                  curve: Curves.easeInOut,\n                  top: 0,\n                  bottom: 0,\n                  right: _showEpisodePanel ? 0 : -350,\n                  width: 350,\n                  child: GlassContainer(', 'if (!_isPiPMode)\n                  AnimatedPositioned(\n                  duration: const Duration(milliseconds: 300),\n                  curve: Curves.easeInOut,\n                  top: 0,\n                  bottom: 0,\n                  right: _showEpisodePanel ? 0 : -350,\n                  width: 350,\n                  child: GlassContainer(');

  // 6. PiP Button in Bottom Toolbar
  content = content.replaceFirst('// Fullscreen Button\n                                            IconButton(\n                                              icon: Icon(\n                                                _isFullscreen\n                                                    ? Icons.fullscreen_exit\n                                                    : Icons.fullscreen,', '// PiP Button\n                                            IconButton(\n                                              icon: const Icon(Icons.picture_in_picture_alt, color: Colors.white, size: 20),\n                                              onPressed: _togglePiPMode,\n                                              tooltip: \'Chế độ PiP\',\n                                            ),\n                                            const SizedBox(width: 10),\n                                            // Fullscreen Button\n                                            IconButton(\n                                              icon: Icon(\n                                                _isFullscreen\n                                                    ? Icons.fullscreen_exit\n                                                    : Icons.fullscreen,');

  // 7. Simplify controls in PiP mode
  content = content.replaceFirst('// YouTube Red Seekbar with Hover Time Tooltip\n                                  MouseRegion(', 'if (!_isPiPMode)\n                                  // YouTube Red Seekbar with Hover Time Tooltip\n                                  MouseRegion(');
  
  content = content.replaceFirst('// YouTube Button Row\n                                  Row(\n                                    children: [\n                                      // Play / Pause Circle Pill', 'if (_isPiPMode)\n                                    Row(\n                                      mainAxisAlignment: MainAxisAlignment.center,\n                                      children: [\n                                        IconButton(\n                                          icon: Icon(\n                                            _isPlaying ? Icons.pause : Icons.play_arrow,\n                                            color: Colors.white,\n                                            size: 40,\n                                          ),\n                                          onPressed: () => player.playOrPause(),\n                                        ),\n                                        const SizedBox(width: 20),\n                                        IconButton(\n                                          icon: const Icon(\n                                            Icons.fullscreen,\n                                            color: Colors.white,\n                                            size: 40,\n                                          ),\n                                          onPressed: _togglePiPMode,\n                                        ),\n                                      ],\n                                    ),\n                                  if (!_isPiPMode)\n                                  // YouTube Button Row\n                                  Row(\n                                    children: [\n                                      // Play / Pause Circle Pill');

  file.writeAsStringSync(content);
  print('Done patching player_screen.dart!');
}
