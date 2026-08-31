import os

hdir = r"C:\Users\Asus\AppData\Roaming\Cursor\User\History"

found = []
for root, dirs, files in os.walk(hdir):
    for f in files:
        if f == 'entries.json': continue
        path = os.path.join(root, f)
        try:
            content = open(path, 'r', encoding='utf-8', errors='replace').read()
            if 'settings_screen.dart' in content or 'SettingsScreen' in content or '_accountKey' in content:
                found.append((path, os.path.getmtime(path), len(content)))
        except Exception as e:
            pass

found.sort(key=lambda x: x[1], reverse=True)
for p, t, l in found[:20]:
    print(f"{p} - Time: {t} - Len: {l}")
