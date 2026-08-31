import os

history_dirs = [
    r"C:\Users\Asus\AppData\Roaming\Code\User\History",
    r"C:\Users\Asus\AppData\Roaming\Cursor\User\History"
]

found = []
for hdir in history_dirs:
    if not os.path.exists(hdir): continue
    for root, dirs, files in os.walk(hdir):
        for f in files:
            path = os.path.join(root, f)
            try:
                content = open(path, 'r', encoding='utf-8').read()
                if 'class SettingsScreen' in content:
                    found.append((path, os.path.getmtime(path), len(content)))
            except:
                pass

found.sort(key=lambda x: x[1], reverse=True)
for p, t, l in found[:20]:
    print(f"{p} - Time: {t} - Len: {l}")
