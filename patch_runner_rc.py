path = r"T:\Project\Phim\mytv4u_flutter\windows\runner\Runner.rc"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "IDI_AUDIO_ICON" not in content:
    content = content.replace('IDI_APP_ICON            ICON                    "resources\\\\app_icon.ico"', 
                              'IDI_APP_ICON            ICON                    "resources\\\\app_icon.ico"\nIDI_AUDIO_ICON          ICON                    "resources\\\\audio.ico"')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added audio icon to Runner.rc")
else:
    print("Already added")
