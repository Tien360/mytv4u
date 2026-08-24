with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "L10n.t('health_utilities')" in line:
        start_idx = i
    if "SizedBox(key: _languageKey)" in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    for i in range(start_idx, end_idx):
        print(f"{i}: {lines[i].strip()}")
