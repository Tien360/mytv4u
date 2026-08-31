path = r"T:\Project\Phim\mytv4u_flutter\windows\runner\resource.h"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "IDI_AUDIO_ICON" not in content:
    content = content.replace("#define IDI_APP_ICON                    101", "#define IDI_APP_ICON                    101\n#define IDI_AUDIO_ICON                  102")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added IDI_AUDIO_ICON to resource.h")
else:
    print("Already added")
