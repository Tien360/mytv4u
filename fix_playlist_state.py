import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# 1. Add _playlistFiles to State and initialize it
old_init = '''  class _AudioPlayerScreenState extends State<AudioPlayerScreen> with TickerProviderStateMixin {
    late final Player player;
    int currentIndex = 0;'''
new_init = '''  class _AudioPlayerScreenState extends State<AudioPlayerScreen> with TickerProviderStateMixin {
    late List<PlatformFile> _playlistFiles;
    late final Player player;
    int currentIndex = 0;'''
content = content.replace(old_init, new_init)

old_init_state = '''  void initState() {
    super.initState();
    currentIndex = widget.initialIndex;'''
new_init_state = '''  void initState() {
    super.initState();
    _playlistFiles = List.from(widget.files);
    currentIndex = widget.initialIndex;'''
content = content.replace(old_init_state, new_init_state)

# Replace all widget.files with _playlistFiles inside the state class
# (but not in the AudioPlayerScreen class definition)
content = content.replace('widget.files.length', '_playlistFiles.length')
content = content.replace('widget.files[currentIndex]', '_playlistFiles[currentIndex]')
content = content.replace('widget.files[index]', '_playlistFiles[index]')

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
