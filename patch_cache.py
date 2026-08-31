import re

def revert_4k_and_increase_cache(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove 4K texture cap
    content = content.replace("width: 3840, height: 2160, ", "")

    # 2. Increase cache to 500MB+ for >8GB RAM
    # Current code:
    # if (_systemRamMB > 8192) {
    #   bufferSize = 128 * 1024 * 1024;
    #   demuxerMaxBytes = '256M';
    #   demuxerMaxBackBytes = '128M';
    # }
    
    pattern_buffer = r"if \(_systemRamMB > 8192\) \{\s*bufferSize = 128 \* 1024 \* 1024;\s*demuxerMaxBytes = '256M';\s*demuxerMaxBackBytes = '128M';\s*\}"
    replacement_buffer = '''if (_systemRamMB > 8192) {
      bufferSize = 512 * 1024 * 1024; // 512MB
      demuxerMaxBytes = '1024M'; // 1GB Cache
      demuxerMaxBackBytes = '512M';
    }'''
    
    content = re.sub(pattern_buffer, replacement_buffer, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

revert_4k_and_increase_cache('lib/screens/player_screen.dart')
revert_4k_and_increase_cache('lib/screens/tv_player_screen.dart')
print("Patched 8K and increased cache to 512MB/1GB")
