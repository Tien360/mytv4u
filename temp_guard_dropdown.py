import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

sleep_timer_search = "value: _audioSleepTimer,"
sleep_timer_replace = "value: [0, 15, 30, 60, 120].contains(_audioSleepTimer) ? _audioSleepTimer : 0,"
if sleep_timer_search in content:
    content = content.replace(sleep_timer_search, sleep_timer_replace)
    print("Guarded _audioSleepTimer!")
else:
    print("Could not find _audioSleepTimer")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
