import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the setProperty block
    pattern = r"platform\.setProperty\('demuxer-max-bytes',\s*'64M'\);\s*platform\.setProperty\('demuxer-max-back-bytes',\s*'32M'\);"
    
    new_props = '''platform.setProperty('demuxer-max-bytes', demuxerMaxBytes);
      platform.setProperty('demuxer-max-back-bytes', demuxerMaxBackBytes);
      
      // Tối ưu 8K / HLS
      platform.setProperty('vd-lavc-threads', '16'); // Huy động CPU đa luồng
      platform.setProperty('vo', 'gpu-next'); // Engine render thế hệ mới (nét & mượt hơn)
      platform.setProperty('framedrop', 'decoder'); // Cho phép rớt frame để chống đứng máy khi tải quá nặng'''

    content = re.sub(pattern, new_props, content, flags=re.MULTILINE)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_file('lib/screens/player_screen.dart')
patch_file('lib/screens/tv_player_screen.dart')
print("Regex Patched both player screens!")
