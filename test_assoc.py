import winreg

def add_open_with():
    exe_path = r'T:\Project\Phim\mytv4u_flutter\build\windows\x64\runner\Release\MyTV4U.exe'
    prog_id = 'MyTV4U.MediaFile'
    
    # Register ProgID
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, fr'Software\Classes\{prog_id}')
    winreg.SetValue(key, '', winreg.REG_SZ, 'MyTV4U Media File')
    
    cmd_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, fr'Software\Classes\{prog_id}\shell\open\command')
    winreg.SetValue(cmd_key, '', winreg.REG_SZ, f'"{exe_path}" "%1"')
    
    # Add to extensions
    extensions = ['.mp4', '.mkv', '.avi', '.flv', '.webm', '.mov', '.ts', '.mp3', '.m4a', '.wav', '.flac', '.aac']
    for ext in extensions:
        try:
            ext_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, fr'Software\Classes\{ext}\OpenWithProgids')
            winreg.SetValueEx(ext_key, prog_id, 0, winreg.REG_NONE, b'')
        except Exception as e:
            print(f'Error adding {ext}: {e}')

add_open_with()
print('Added to OpenWithProgids')
