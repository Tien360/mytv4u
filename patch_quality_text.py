import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the old multi-badge injection
old_badges = """if (_premiumMetadata != null) ...[
                                                if (_premiumMetadata!['resolution'] != null)
                                                  _buildBadge(
                                                    _premiumMetadata!['resolution'].toString().split(' ')[0],
                                                    Colors.greenAccent,
                                                  ),
                                                if (_premiumMetadata!['hdr'] != null && _premiumMetadata!['hdr'] != 'SDR')
                                                  _buildBadge(
                                                    _premiumMetadata!['hdr'],
                                                    Colors.purpleAccent,
                                                  ),
                                                if (_premiumMetadata!['audioTracks'] != null && (_premiumMetadata!['audioTracks'] as List).isNotEmpty)
                                                  _buildBadge(
                                                    (_premiumMetadata!['audioTracks'] as List).first['name'] ?? 'Audio',
                                                    Colors.blueAccent,
                                                  ),
                                              ] else if (_movie!.quality.isNotEmpty)
                                                _buildBadge(
                                                  _movie!.quality,
                                                  Colors.greenAccent,
                                                ),"""

new_badges = """if (_premiumMetadata != null) 
                                                _buildBadge(
                                                  _getPremiumQualityText(),
                                                  Colors.greenAccent,
                                                )
                                              else if (_movie!.quality.isNotEmpty)
                                                _buildBadge(
                                                  _movie!.quality,
                                                  Colors.greenAccent,
                                                ),"""

if old_badges in content:
    content = content.replace(old_badges, new_badges)
    
    # Add _getPremiumQualityText() method
    helper_code = """
  String _getPremiumQualityText() {
    if (_premiumMetadata == null) return '';
    String res = (_premiumMetadata!['resolution'] ?? '').toString().split(' ')[0];
    String hdr = (_premiumMetadata!['hdr'] ?? '').toString();
    
    String audio = '';
    if (_premiumMetadata!['audioTracks'] != null && (_premiumMetadata!['audioTracks'] as List).isNotEmpty) {
      String codec = (_premiumMetadata!['audioTracks'] as List).first['codec'] ?? '';
      String codecUpper = codec.toUpperCase();
      if (codecUpper.contains('ATMOS')) audio = 'Atmos';
      else if (codecUpper.contains('TRUEHD')) audio = 'TrueHD';
      else if (codecUpper.contains('DOLBY DIGITAL PLUS') || codecUpper.contains('EAC3') || codecUpper.contains('DD+')) audio = 'DD+';
      else if (codecUpper.contains('DOLBY DIGITAL') || codecUpper.contains('AC3')) audio = 'DD';
      else if (codecUpper.contains('DTS-HD MA')) audio = 'DTS-HD MA';
      else if (codecUpper.contains('DTS-HD')) audio = 'DTS-HD';
      else if (codecUpper.contains('DTS')) audio = 'DTS';
      else if (codecUpper.contains('AAC')) audio = 'AAC';
      else audio = codec.split(' ')[0];
    }
    
    List<String> parts = [];
    if (res.isNotEmpty && res != 'Unknown') parts.add(res);
    if (hdr.isNotEmpty && hdr != 'Unknown') parts.add(hdr);
    if (audio.isNotEmpty && audio != 'Unknown') parts.add(audio);
    
    return parts.join(' ');
  }

  void _fetchDetail() {"""
    
    content = content.replace("  void _fetchDetail() {", helper_code)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched premium quality badge to single combined text")
else:
    print("Could not find old badges to replace")
