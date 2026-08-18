import os
import re

filepath = 'lib/screens/player_screen.dart'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# We need to find the ListView for Secondary Subtitle.
# In player_screen.dart, it's under // Tab Phụ đề phụ. Wait, mojibake // Tab Phá»¥ Ä‘á»  phá»¥
# Let's search for L10n.t('add_external_sub') inside the ListView children and insert the ListTile.
# There are two dd_external_sub buttons (one for main, one for secondary).
# The main one is followed by _subtitleTracks. The secondary one is followed by ..._subtitleTracks, ..._openSubtitles and _selectedSecondarySubtitleTrack.

# Let's inject a ListTile before the OutlinedButton for secondary subtitle.
# Since we can't easily match exactly with simple replace due to formatting, let's look for _selectSecondarySubtitleTrack.
# Actually, the button is:
'''
                              OutlinedButton.icon(
                                onPressed: _addExternalSubtitle,
                                icon: const Icon(Icons.add),
                                label: Text(L10n.t('add_external_sub')),
'''

# Let's write a targeted script to inject into player_screen.dart.
# Find Tab(icon: Icon(Icons.info_outline), text: L10n.t('tab_info')), 
# Oh wait, the contents are in TabBarView.
# 1st: Tab Chung
# 2nd: Tab Audio -> contains L10n.t('sync_audio')
# 3rd: Tab Sub Main -> contains L10n.t('sync_subtitle')
# 4th: Tab Sub Sec -> lacks sync button!

# Let's just find where _selectedSecondarySubtitleTrack is used and inject before the OutlinedButton.
target = '''                          ListView(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 24,
                              vertical: 16,
                            ),
                            children: ['''

new_target = '''                          ListView(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 24,
                              vertical: 16,
                            ),
                            children: [
                              ListTile(
                                leading: const Icon(Icons.sync, color: Colors.blueAccent),
                                title: Text(L10n.t('sync_subtitle')),
                                trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                                onTap: () {
                                  Navigator.pop(context);
                                  setState(() => _activePanel = SidePanelMode.secondarySubtitle);
                                },
                              ),
                              const Divider(color: Colors.white24),'''

# Wait, there are 5 ListView's in the TabBarView.
# The 4th one is the secondary subtitle.
# Let's just split by ListView( inside the TabBarView block.
parts = text.split('ListView(')
# parts[0] is everything up to the first ListView (Tab Chung)
# parts[1] is Tab Chung
# parts[2] is Tab Audio
# parts[3] is Tab Sub Main
# parts[4] is Tab Sub Sec

if len(parts) >= 6:
    # Inject into parts[4]
    parts[4] = parts[4].replace('''
                            padding: const EdgeInsets.symmetric(
                              horizontal: 24,
                              vertical: 16,
                            ),
                            children: [
''', '''
                            padding: const EdgeInsets.symmetric(
                              horizontal: 24,
                              vertical: 16,
                            ),
                            children: [
                              ListTile(
                                leading: const Icon(Icons.sync, color: Colors.blueAccent),
                                title: Text(L10n.t('sync_subtitle')),
                                trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                                onTap: () {
                                  Navigator.pop(context);
                                  setState(() => _activePanel = SidePanelMode.secondarySubtitle);
                                },
                              ),
                              const Divider(color: Colors.white24),
''', 1)

    text = 'ListView('.join(parts)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Injected secondary subtitle sync button.")
else:
    print(f"Error: Found {len(parts)} ListView splits.")

