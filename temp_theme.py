import sys, re
with open('lib/main.dart', 'r', encoding='utf-8') as f:
    c = f.read()

new_theme_part = """          useMaterial3: true,
          pageTransitionsTheme: const PageTransitionsTheme(
            builders: {
              TargetPlatform.windows: ZoomPageTransitionsBuilder(allowSnapshotting: false),
            },
          ),"""

c = re.sub(r'useMaterial3:\s*true,', new_theme_part, c)

with open('lib/main.dart', 'w', encoding='utf-8') as f:
    f.write(c)
print("Regex replaced useMaterial3")
