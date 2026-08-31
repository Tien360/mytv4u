import re

def add_width_height(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r"(controller = VideoController\(\s*player,\s*configuration: VideoControllerConfiguration\(\s*)(enableHardwareAcceleration: _hwAccel,)(\s*\),\s*\);)"
    
    # We will set the texture rendering target to a maximum of 4K.
    # This prevents the Flutter Engine from being choked by a 33MB+ 8K texture copy every frame (60fps), 
    # which causes massive stuttering on any CPU/GPU combo.
    replacement = r"\1width: 3840, height: 2160, \2\3"
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

add_width_height('lib/screens/player_screen.dart')
add_width_height('lib/screens/tv_player_screen.dart')
print("Patched VideoControllerConfiguration")
