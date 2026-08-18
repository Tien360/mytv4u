import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''                            const SizedBox(height: 48),
                            
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                _buildSectionTitle(Icons.source, L10n.t('movie_sources')),'''
replacement = '''                            const SizedBox(height: 48),

                            _buildSectionTitle(Icons.color_lens, 'Màu sắc Video (Toàn cục)'),
                            const SizedBox(height: 16),
                            if (_prefs != null)
                              GlassContainer(
                                padding: const EdgeInsets.all(16),
                                borderRadius: 16,
                                color: Colors.white.withOpacity(0.05),
                                borderColor: Colors.white.withOpacity(0.1),
                                child: GlobalColorSettings(
                                  prefs: _prefs!,
                                  onSettingsChanged: (data) => _syncToFirebase(),
                                ),
                              ),
                            
                            const SizedBox(height: 48),
                            
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                _buildSectionTitle(Icons.source, L10n.t('movie_sources')),'''
content = content.replace(target, replacement)

# Add import
if "import '../widgets/global_color_settings.dart';" not in content:
    content = content.replace("import '../widgets/glass_container.dart';", "import '../widgets/glass_container.dart';\nimport '../widgets/global_color_settings.dart';")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched successfully')
