import re

def optimize_8k_mpv_v2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r"platform\.setProperty\('demuxer-lavf-o-append', 'fflags\=\+fastseek'\);"
    
    replacement = '''platform.setProperty('demuxer-lavf-o-append', 'fflags=+fastseek');
      
      // -- TỐI ƯU HÓA 8K TẬN RĂNG BỞI AI --
      platform.setProperty('profile', 'fast'); // Tắt bộ lọc làm đẹp
      platform.setProperty('vd-lavc-dr', 'yes'); // Direct Rendering
      platform.setProperty('hwdec', 'd3d11va'); // Force D3D11VA
      platform.setProperty('vd-lavc-threads', '24'); // Max threads
      platform.setProperty('d3d11-exclusive-fs', 'yes');'''
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

optimize_8k_mpv_v2('lib/screens/player_screen.dart')
optimize_8k_mpv_v2('lib/screens/tv_player_screen.dart')
print("Patched extreme 8K optimizations v2")
