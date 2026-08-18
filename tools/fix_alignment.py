import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the specific SizedBox before DropdownButton for Color and Font with Spacer
text = re.sub(r"Text\(L10n\.t\('sub_color'\), .*?\n\s*const SizedBox\(width: 16\),",
              r"Text(L10n.t('sub_color'), style: const TextStyle(color: Colors.white, fontSize: 16)),\n                                      const Spacer(),", text)

text = re.sub(r"Text\(L10n\.t\('sub_font'\), .*?\n\s*const SizedBox\(width: 16\),",
              r"Text(L10n.t('sub_font'), style: const TextStyle(color: Colors.white, fontSize: 16)),\n                                      const Spacer(),", text)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated Spacers in settings_screen.dart')
