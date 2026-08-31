def optimize_8k_mpv_v3(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target = "platform.setProperty('demuxer-lavf-o-append', 'fflags=+fastseek');"
    
    replacement = '''platform.setProperty('demuxer-lavf-o-append', 'fflags=+fastseek');
      
      // -- TỐI ƯU HÓA 8K TẬN RĂNG BỞI AI --
      platform.setProperty('profile', 'fast'); // Tắt bộ lọc làm đẹp
      platform.setProperty('vd-lavc-dr', 'yes'); // Direct Rendering
      platform.setProperty('hwdec', 'auto-copy'); // An toàn cho Optimus
      platform.setProperty('vd-lavc-threads', '32'); // Max threads
      platform.setProperty('d3d11-exclusive-fs', 'yes');'''
    
    content = content.replace(target, replacement)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

optimize_8k_mpv_v3('lib/screens/player_screen.dart')
optimize_8k_mpv_v3('lib/screens/tv_player_screen.dart')
print("Patched extreme 8K optimizations v3")
