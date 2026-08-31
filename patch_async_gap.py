import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\widgets\spider_easter_egg.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_show = """  static void show(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final easterEggsEnabled = prefs.getBool('easterEggs') ?? true;
    if (!easterEggsEnabled) return;

    if (_isPlaying) return;
    _isPlaying = true;

    final int effectType = _random.nextInt(3) + 1; // 1, 2, or 3
    final overlayState = Overlay.of(context);"""

new_show = """  static void show(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final easterEggsEnabled = prefs.getBool('easterEggs') ?? true;
    if (!easterEggsEnabled) return;
    if (!context.mounted) return;

    if (_isPlaying) return;
    _isPlaying = true;

    final int effectType = _random.nextInt(3) + 1; // 1, 2, or 3
    final overlayState = Overlay.of(context);"""

content = content.replace(old_show, new_show)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed BuildContext async gap")
