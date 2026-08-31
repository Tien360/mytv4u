import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

old_build = '''  @override
  Widget build(BuildContext context) {
    bool isPodcast = duration.inMinutes >= 30;

    return Listener(
      onPointerDown: (event) {
        if (event.buttons == 2) { // Right click
          _showAudioSettings();
        }
      },
      child: Scaffold('''
      
new_build = '''  @override
  Widget build(BuildContext context) {
    bool isPodcast = duration.inMinutes >= 30;

    return Focus(
      autofocus: true,
      onKeyEvent: (node, event) {
        if (event is KeyDownEvent) {
          if (event.logicalKey == LogicalKeyboardKey.escape) {
            Navigator.pop(context);
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.space) {
            isPlaying ? player.pause() : player.play();
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.arrowRight) {
            player.seek(position + const Duration(seconds: 10));
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.arrowLeft) {
            player.seek(position - const Duration(seconds: 10));
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.keyN) {
            _next();
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.keyP) {
            _prev();
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.keyM) {
            player.setVolume(player.state.volume > 0 ? 0 : 100);
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.keyS) {
            _toggleShuffle();
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.keyR) {
            _toggleRepeat();
            return KeyEventResult.handled;
          }
        }
        return KeyEventResult.ignored;
      },
      child: Listener(
        onPointerDown: (event) {
          if (event.buttons == 2) { // Right click
            _showAudioSettings();
          }
        },
        child: Scaffold('''

content = content.replace(old_build, new_build)

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
