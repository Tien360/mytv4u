import re

def full_fix(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Fix custom string
    text = text.replace("L10n.t('custom')", "'custom'")
    
    # Fix Text(p)
    text = text.replace("Text(p)", "Text(L10n.t(p) ?? p)")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

full_fix('lib/widgets/global_color_settings.dart')
full_fix('lib/widgets/advanced_controls_panel.dart')

print("Fully fixed")
