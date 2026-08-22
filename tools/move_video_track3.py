
import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure length is 5
text = text.replace('length: 6,', 'length: 5,')

# Remove any stray Tab(icon: Icon(Icons.hd)...) if it exists
tab_header_pattern = r'\s*Tooltip\(\s*message:[^\n]+(_selectedVideoTrack)[^\n]+L10n\.t[^\n]+\n\s*\),\s*\n\s*\),\s*'
text = re.sub(tab_header_pattern, '', text, flags=re.DOTALL)

# Add to General Tab
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
text = re.sub(r'(// Tab Chung.*?children: \[)', r'\1\n' + new_list_tile, text, flags=re.DOTALL)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done')

