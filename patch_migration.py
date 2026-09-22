import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

migration_code = """    List<String> enabledSources = prefs.getStringList('enabled_sources') ?? [
      'premium',
      'nguonc',
      'ophim',
      'kkphim',
      'vsmov',
      'film4knet',
      'free2',
      'free1',
      'motchill',
    ];
    if (enabledSources.contains('phim4k')) {
       enabledSources = enabledSources.map((e) => e == 'phim4k' ? 'free2' : e).toList();
       prefs.setStringList('enabled_sources', enabledSources);
    }"""

# We need to replace all `final enabledSources = prefs.getStringList('enabled_sources') ?? [ ... ];`
pattern = r"final\s+enabledSources\s*=\s*prefs\.getStringList\('enabled_sources'\)\s*\?\?\s*\[.*?\];"
content = re.sub(pattern, migration_code, content, flags=re.DOTALL)

with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(content)

print("Added migration logic to phim_api.dart")
