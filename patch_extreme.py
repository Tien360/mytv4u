import re

def optimize_8k_mpv(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r"platform\.setProperty\('vd-lavc-threads', '16'\); // 16 luong CPU gank 8K neu hwdec that bai"
    
    replacement = '''platform.setProperty('vd-lavc-threads', '24'); // Max threads
      
      // -- TỐI ƯU HÓA 8K TẬN RĂNG BỞI AI --
      platform.setProperty('profile', 'fast'); // Tắt các bộ lọc làm đẹp (deband, scaler...) không cần thiết cho 8K
      platform.setProperty('vd-lavc-dr', 'yes'); // Direct Rendering: Bỏ qua 1 bước copy dữ liệu trong VRAM
      platform.setProperty('hwdec', 'd3d11va'); // Ép dùng D3D11VA thay vì DXVA2 cũ kĩ
      platform.setProperty('d3d11-exclusive-fs', 'yes');'''
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

optimize_8k_mpv('lib/screens/player_screen.dart')
optimize_8k_mpv('lib/screens/tv_player_screen.dart')
print("Patched 8K extreme optimizations")
