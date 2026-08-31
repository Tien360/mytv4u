def restore_4k_cap(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target = "configuration: VideoControllerConfiguration(\n        enableHardwareAcceleration: _hwAccel,"
    replacement = "configuration: VideoControllerConfiguration(\n        width: 3840, height: 2160, \n        enableHardwareAcceleration: _hwAccel,"
    
    if "width: 3840" not in content:
        content = content.replace(target, replacement)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

restore_4k_cap('lib/screens/player_screen.dart')
restore_4k_cap('lib/screens/tv_player_screen.dart')
print("Restored 4K cap")
