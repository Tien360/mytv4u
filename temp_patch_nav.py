import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/main_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

nav_search = """                        await Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const SettingsScreen(),
                          ),
                        );"""
nav_replace = """                        await Navigator.push(
                          context,
                          PageRouteBuilder(
                            opaque: false,
                            pageBuilder: (_, __, ___) => const SettingsScreen(),
                          ),
                        );"""
if nav_search in content:
    content = content.replace(nav_search, nav_replace)
    print("Replaced Navigator in main_screen!")
else:
    print("Could not find Navigator.push")

with open('lib/screens/main_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
