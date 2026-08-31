import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

if 'palette_generator.dart' not in content:
    content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport 'package:palette_generator/palette_generator.dart';")

content = content.replace('Color _dominantColor = Colors.blueAccent;', '')
content = content.replace('Uint8List? coverArt;', 'Uint8List? coverArt;\n  Color _dominantColor = Colors.blueAccent;')
content = content.replace('AudioVisualizer(isPlaying: isPlaying, type: visualizerType)', 'AudioVisualizer(isPlaying: isPlaying, type: visualizerType, color: _dominantColor)')
content = content.replace("AudioVisualizer(type: 'inline')", "AudioVisualizer(type: 'inline', color: _dominantColor)")

old_art = '''      if (tags.pictures.isNotEmpty) {
        coverArt = Uint8List.fromList(tags.pictures.first.imageData);
        _coverCache[file.path!] = coverArt;
      }
    } catch (e) {
      // Ignore
    }'''
new_art = '''      if (tags.pictures.isNotEmpty) {
        coverArt = Uint8List.fromList(tags.pictures.first.imageData);
        _coverCache[file.path!] = coverArt;
      }
    } catch (e) {
      // Ignore
    }
    _updateDominantColor();'''
content = content.replace(old_art, new_art)

method_code = '''  Future<void> _updateDominantColor() async {
    if (coverArt == null) {
      if (mounted) setState(() => _dominantColor = Colors.blueAccent);
      return;
    }
    try {
      final PaletteGenerator generator = await PaletteGenerator.fromImageProvider(
        MemoryImage(coverArt!),
        size: const Size(100, 100),
      );
      if (mounted) {
        setState(() {
          _dominantColor = generator.dominantColor?.color ?? generator.vibrantColor?.color ?? Colors.blueAccent;
        });
      }
    } catch (e) {
      if (mounted) setState(() => _dominantColor = Colors.blueAccent);
    }
  }

  void _next() {'''
content = content.replace('  void _next() {', method_code)

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
