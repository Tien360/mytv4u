import re

def fix_presets(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    text = re.sub(r"L10n\.t\('([^']+)'\):\s*\{", r"'\1': {", text)
    text = re.sub(r"_preset = L10n\.t\('default'\)", r"_preset = 'default'", text)
    text = re.sub(r"getString\('color_preset'\) \?\? L10n\.t\('default'\)", r"getString('color_preset') ?? 'default'", text)
    
    # Text(preset, -> Text(L10n.t(preset) ?? preset, 
    # But wait, let's be more specific. In global_color_settings.dart:
    text = text.replace("Text(preset,", "Text(L10n.t(preset) ?? preset,")
    # For active button:
    text = text.replace("Text(_preset,", "Text(L10n.t(_preset) ?? _preset,")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

fix_presets('lib/widgets/global_color_settings.dart')
fix_presets('lib/widgets/advanced_controls_panel.dart')

print("Done presets map")
