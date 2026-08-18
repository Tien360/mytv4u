import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''                          if (_currentUser != null)
                            _buildUserCard()
                          else
                            _buildLoginCard(),
                          
                          const SizedBox(height: 48),

                          _buildSectionTitle(Icons.color_lens, L10n.t('global_color_settings') ?? 'Cài đặt màu toàn cục'),
                          const SizedBox(height: 16),
                          const GlobalColorSettings(),
                          
                          const SizedBox(height: 48),'''

content = content.replace('''                          if (_currentUser != null)
                            _buildUserCard()
                          else
                            _buildLoginCard(),
                          
                          const SizedBox(height: 48),''', replacement)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched settings_screen.dart')
