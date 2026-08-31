import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# Replace class _AudioPlayerScreenState ...
old_class = '''class _AudioPlayerScreenState extends State<AudioPlayerScreen> with TickerProviderStateMixin {
  late final Player player;'''
new_class = '''class _AudioPlayerScreenState extends State<AudioPlayerScreen> with TickerProviderStateMixin {
  late List<PlatformFile> _playlistFiles;
  late final Player player;'''
content = content.replace(old_class, new_class)

old_init2 = '''  @override
  void initState() {
    super.initState();
    currentIndex = widget.initialIndex;'''
new_init2 = '''  @override
  void initState() {
    super.initState();
    _playlistFiles = List.from(widget.files);
    currentIndex = widget.initialIndex;'''
content = content.replace(old_init2, new_init2)

content = content.replace('widget.files.length', '_playlistFiles.length')
content = content.replace('widget.files[currentIndex]', '_playlistFiles[currentIndex]')
content = content.replace('widget.files[index]', '_playlistFiles[index]')

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
