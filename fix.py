lines = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read().splitlines()

# The messed up part starts at line 794. Let's find exactly what to remove!
# Line 781 is ListTile(
# Line 793 is ),  (the end of Switch)
# Lines 794 to 899 are the mistakenly inserted settings.
# Line 900 is const Divider(color: Colors.white12, height: 32),

del lines[793:899]

# Wait, if we delete lines 793 to 898 (inclusive), 
# Actually, the original code at line 793 was `                                          ),` which closed the Switch.
# Then we should close the ListTile with `                                        ),`
# Let's just fix it properly using Python.
