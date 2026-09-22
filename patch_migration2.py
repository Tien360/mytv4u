import re

with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

migration_code = """      List<String>? savedSources = prefs.getStringList('enabled_sources');
      if (savedSources != null && savedSources.contains('phim4k')) {
         savedSources = savedSources.map((e) => e == 'phim4k' ? 'free2' : e).toList();
         prefs.setStringList('enabled_sources', savedSources);
      }
      
      final enabledSources = savedSources ??
          [
            'premium',
            'nguonc',
            'ophim',
            'kkphim',
            'vsmov',
            'film4knet',
            'free2',
            'free1',
            'motchill',
          ];"""

pattern = r"final\s+enabledSources\s*=\s*prefs\.getStringList\('enabled_sources'\)\s*\?\?\s*\[.*?\];"
content = re.sub(pattern, migration_code, content, flags=re.DOTALL)

with open("lib/screens/settings_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)

print("Added migration logic to settings_screen.dart")
