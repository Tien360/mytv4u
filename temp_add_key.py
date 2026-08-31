import sys
with open('lib/screens/main_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("GlobalKey<SportScreenState>();", "GlobalKey<SportScreenState>();\n  final GlobalKey<dynamic> _gamingKey = GlobalKey();")

with open('lib/screens/main_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)
print("added _gamingKey")
