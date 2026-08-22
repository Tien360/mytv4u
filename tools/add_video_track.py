
import sys
with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Variables
text = text.replace(
'''  List<AudioTrack> _audioTracks = [];''',
'''  List<VideoTrack> _videoTracks = [];
  List<AudioTrack> _audioTracks = [];''')

text = text.replace(
'''  AudioTrack? _selectedAudioTrack;''',
'''  VideoTrack? _selectedVideoTrack;
  AudioTrack? _selectedAudioTrack;''')

# Listener 1
text = text.replace(
'''            _audioTracks = tracks.audio;''',
'''            _videoTracks = tracks.video;
            _audioTracks = tracks.audio;''')

# Listener 2
text = text.replace(
'''            _selectedAudioTrack = track.audio;''',
'''            _selectedVideoTrack = track.video;
            _selectedAudioTrack = track.audio;''')

# Initial clear
text = text.replace(
'''      _audioTracks = [];''',
'''      _videoTracks = [];
      _audioTracks = [];''')
text = text.replace(
'''      _selectedAudioTrack = null;''',
'''      _selectedVideoTrack = null;
      _selectedAudioTrack = null;''')

# Selection method
selection_method = '''  void _selectVideoTrack(VideoTrack track) {
    setState(() => _selectedVideoTrack = track);
    player.setVideoTrack(track);
    if (Navigator.canPop(context)) Navigator.pop(context);
  }

  void _selectAudioTrack(AudioTrack track) {'''
text = text.replace('  void _selectAudioTrack(AudioTrack track) {', selection_method)

# Helper method
helper_method = '''  String _getVideoTrackName(VideoTrack track) {
    if (track.id == 'auto') return L10n.t('auto_default') ?? 'Tự động (Mặc định)';
    if (track.id == 'no') return L10n.t('off') ?? 'Tắt';
    if (track.w != null && track.h != null) {
      return 'x';
    }
    return track.title ?? track.id ?? L10n.t('unknown') ?? 'Không rõ';
  }

  String _getTrackFullName(dynamic track) {'''
text = text.replace('  String _getTrackFullName(dynamic track) {', helper_method)

# Dialog tab length
text = text.replace('                  length: 5,', '                  length: 6,')

# Tab Header
tab_header = '''                          Tab(icon: Icon(Icons.speed), text: L10n.t('tab_general')),
                          Tooltip(
                            message: (L10n.t('currently_selected') ?? 'Selected: ') + (_selectedVideoTrack != null ? _getVideoTrackName(_selectedVideoTrack!) : (L10n.t('auto') ?? 'Auto')),
                            child: Tab(
                              icon: Icon(Icons.hd),
                              text: L10n.t('tab_video') ?? 'Chất lượng',
                            ),
                          ),'''
text = text.replace('''                          Tab(icon: Icon(Icons.speed), text: L10n.t('tab_general')),''', tab_header)

# Tab Content
tab_content = '''                            // Tab Chất lượng
                            ListView(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 24,
                                vertical: 16,
                              ),
                              children: [
                                Text(
                                  L10n.t('select_video_quality') ?? 'Chọn chất lượng Video',
                                  style: const TextStyle(
                                    color: Colors.white70,
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 16),
                                ..._videoTracks.map((track) {
                                  final isSelected =
                                      track.id == _selectedVideoTrack?.id;
                                  return HoverableTrackItem(
                                    title: _getVideoTrackName(track),
                                    isSelected: isSelected,
                                    onTap: () => _selectVideoTrack(track),
                                  );
                                }),
                              ],
                            ),
                            // Tab Âm thanh'''
text = text.replace('                            // Tab Âm thanh', tab_content)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done')

