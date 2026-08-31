content = open('lib/widgets/optimizer_dialog.dart', 'r', encoding='utf-8').read()
old_eff = """    if (_recAllEffects) {
      await prefs.setBool('minimalist_ui', false);
      isMinimalistUi.value = false;
      await prefs.setBool('enable_ambient_bg', true);
      globalEnableAmbient.value = true;
      await prefs.setBool('enable_easter_eggs', true);
    }"""
new_eff = """    if (_recAllEffects) {
      await prefs.setBool('minimalist_ui', false);
      isMinimalistUi.value = false;
      await prefs.setBool('enable_ambient_bg', true);
      globalEnableAmbient.value = true;
      await prefs.setBool('enable_easter_eggs', true);
      await prefs.setString('audio_visualizer', 'bars');
      await prefs.setBool('audio_vinyl', true);
    }"""
content = content.replace(old_eff, new_eff)

old_eff2 = """                  onChanged: (v) => setState(() {
                    _recAllEffects = v!;
                    if (v) {
                      _recMinimalist = false;
                      _recDisableAmbient = false;
                      _recDisableTrailer = false;
                    }
                  }),"""
new_eff2 = """                  onChanged: (v) => setState(() {
                    _recAllEffects = v!;
                    if (v) {
                      _recMinimalist = false;
                      _recDisableAmbient = false;
                      _recDisableTrailer = false;
                      _recDisableAudioEffects = false;
                    }
                  }),"""
content = content.replace(old_eff2, new_eff2)
open('lib/widgets/optimizer_dialog.dart', 'w', encoding='utf-8').write(content)
