
import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Restore length
text = text.replace('length: 6,', 'length: 5,')

# 2. Remove Tab Header
tab_header_pattern = r'                          Tooltip\(\s*message:\s*\(L10n\.t\(\'currently_selected\'\)[^\n]+(_selectedVideoTrack)[^\n]+L10n\.t\(\'tab_video\'\)[^\n]+\n\s*\),\s*\n\s*\),\s*'
text = re.sub(tab_header_pattern, '', text, flags=re.DOTALL)

# 3. Remove Tab Content
quality_tab_content_pattern = r'                            // Tab Ch.t l..ng.*?// Tab \u00c2m thanh'
text = re.sub(quality_tab_content_pattern, '                            // Tab \u00c2m thanh', text, flags=re.DOTALL)

# 4. Add to General Tab
new_list_tile = '''
                                  if (_videoTracks.isNotEmpty) ...[
                                    ListTile(
                                      title: Text(
                                        L10n.t('tab_video') ?? 'Quality',
                                        style: TextStyle(color: Colors.white),
                                      ),
                                      trailing: DropdownButton<String>(
                                        dropdownColor: Colors.grey[900],
                                        value: _selectedVideoTrack?.id ?? 'auto',
                                        style: const TextStyle(
                                          color: Colors.blueAccent,
                                        ),
                                        items: _videoTracks.map((track) {
                                          return DropdownMenuItem<String>(
                                            value: track.id,
                                            child: Text(_getVideoTrackName(track)),
                                          );
                                        }).toList(),
                                        onChanged: (val) {
                                          if (val != null) {
                                            final track = _videoTracks.firstWhere((t) => t.id == val);
                                            setState(() => _selectedVideoTrack = track);
                                            player.setVideoTrack(track);
                                            setTabState(() {});
                                          }
                                        },
                                      ),
                                    ),
                                    const Divider(color: Colors.white24),
                                  ],
'''
text = re.sub(r'(// Tab General.*?children: \[)', r'\1\n' + new_list_tile, text, flags=re.DOTALL)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done')

