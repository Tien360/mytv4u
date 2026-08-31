content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
keys = ['_accountKey', '_systemKey', '_languageKey', '_sourcesKey', '_videoKey', '_audioKey', '_colorKey', '_subtitleKey', '_shortcutsKey', '_infoKey']
for k in keys:
    key_idx = content.find(f"SizedBox(key: {k})")
    before = content[key_idx-300:key_idx]
    if "Row(" in before:
        print(f"{k} has Row")
