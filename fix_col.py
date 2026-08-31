import re

def fix_collision(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change the import
    content = content.replace("import 'package:youtube_explode_dart/youtube_explode_dart.dart';", "import 'package:youtube_explode_dart/youtube_explode_dart.dart' as yt_explode;")
    
    # Change the usage
    content = content.replace("var yt = YoutubeExplode();", "var yt = yt_explode.YoutubeExplode();")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Fixed collision in player_screen.dart!")

fix_collision('lib/screens/player_screen.dart')
