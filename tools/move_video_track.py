
import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Restore length
text = text.replace('length: 6,', 'length: 5,')

# Remove Quality tab header
tab_header = '''                          Tooltip(
                            message: (L10n.t('currently_selected') ?? 'Selected: ') + (_selectedVideoTrack != null ? _getVideoTrackName(_selectedVideoTrack!) : (L10n.t('auto') ?? 'Auto')),
                            child: Tab(
                              icon: Icon(Icons.hd),
                              text: L10n.t('tab_video') ?? 'Chất lượng',
                            ),
                          ),'''
text = text.replace(tab_header, '')

# Remove Quality tab content
quality_tab_content_pattern = r'// Tab Ch\u1ea5t l\u01b0\u1ee3ng.*?// Tab \u00c2m thanh'
text = re.sub(r'// Tab Ch.t l..ng.*?// Tab .m thanh', '// Tab \u00c2m thanh', text, flags=re.DOTALL)

# Add to General tab
general_tab_pattern = r'(// Tab General.*?children: \[)'
new_list_tile = '''
                                  if (_videoTracks.isNotEmpty) ...[
                                    ListTile(
                                      title: Text(
                                        L10n.t('tab_video') ?? 'Chất lượng Video',
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
text = re.sub(general_tab_pattern, r'\1\n' + new_list_tile, text, flags=re.DOTALL)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done')

