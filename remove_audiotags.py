import os

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

content = content.replace("import 'package:audiotags/audiotags.dart';", "")

old_extract = '''    try {
      Tag? tag = await AudioTags.read(path);
      setState(() {
        title = tag?.title ?? file.name;
        artist = tag?.artist ?? 'Unknown Artist';
        if (tag != null && tag.pictures.isNotEmpty) {
          coverArt = tag.pictures.first.bytes;
        } else {
          coverArt = null;
        }
      });
    } catch (e) {
      setState(() {
        title = file.name;
        artist = 'Unknown Artist';
        coverArt = null;
      });
    }'''

new_extract = '''    setState(() {
      title = file.name;
      artist = 'Unknown Artist';
      coverArt = null;
    });'''

content = content.replace(old_extract, new_extract)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
