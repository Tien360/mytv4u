content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

keys = ['_accountKey', '_systemKey', '_languageKey', '_sourcesKey', '_videoKey', '_audioKey', '_colorKey', '_subtitleKey', '_shortcutsKey', '_infoKey']
indices = []
for key in keys:
    # Find the start of the block. We'll search backwards for const SizedBox(height: 48) or the beginning of the children list.
    idx = content.find(f"SizedBox(key: {key})")
    # Actually, the block starts exactly at SizedBox(key: _...Key) (except for _sourcesKey which has Row before it? Let's check!)
    indices.append((key, idx))

indices.sort(key=lambda x: x[1])
for k, idx in indices:
    print(f"{k}: {idx}")
