import sys

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if line.startswith('  Widget _buildPremiumBadges() {'):
        start_idx = i
        break

if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if lines[i].strip() == 'return _buildInfoBadgesRow(\'\', badges);':
            end_idx = i + 1
            break

if start_idx == -1 or end_idx == -1:
    print("Could not find bounds")
    sys.exit(1)

new_code = """  Widget _buildPremiumBadges() {
    List<Widget> badges = [];
    
    Widget buildTextBadge(String text) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
        decoration: BoxDecoration(border: Border.all(color: Colors.white70), borderRadius: BorderRadius.circular(4)),
        child: Text(text, style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
      );
    }

    const colorFilter = ColorFilter.mode(Colors.white, BlendMode.srcIn);

    if (_currentPremiumMeta != null) {
      String res = (_currentPremiumMeta!['resolution'] ?? '').toString().split(' ')[0];
      String hdr = (_currentPremiumMeta!['hdr'] ?? '').toString();
      if (hdr == 'SDR' || hdr == 'Unknown' || hdr.isEmpty) {
        String fn = (_currentPremiumMeta!['fallback_filename'] ?? '').toString().toUpperCase();
        if (fn.contains('.DV.') || fn.contains('DOLBY VISION') || fn.contains('DOLBY.VISION')) hdr = 'Dolby Vision';
        else if (fn.contains('HDR10+') || fn.contains('HDR10PLUS')) hdr = 'HDR10+';
        else if (fn.contains('HDR10')) hdr = 'HDR10';
        else if (fn.contains('.HDR.') || fn.contains(' HDR ')) hdr = 'HDR';
        else hdr = 'SDR';
      }

      List<String> audioTypes = [];
      if (_currentPremiumMeta!['audioTracks'] != null && (_currentPremiumMeta!['audioTracks'] as List).isNotEmpty) {
        for (var track in (_currentPremiumMeta!['audioTracks'] as List)) {
          String codec = track['codec'] ?? '';
          String codecUpper = codec.toUpperCase();
          String type = '';
          if (codecUpper.contains('ATMOS')) type = 'Atmos';
          else if (codecUpper.contains('TRUEHD')) type = 'TrueHD';
          else if (codecUpper.contains('DOLBY DIGITAL PLUS') || codecUpper.contains('EAC3') || codecUpper.contains('DD+')) type = 'DD+';
          else if (codecUpper.contains('DOLBY DIGITAL') || codecUpper.contains('AC3')) type = 'DD';
          else if (codecUpper.contains('DTS-HD MA') || codecUpper.contains('DTS-HD') || codecUpper.contains('DTS')) type = 'DTS';
          else if (codecUpper.contains('AAC')) type = 'AAC';
          
          if (type.isNotEmpty && !audioTypes.contains(type)) {
            audioTypes.add(type);
          }
        }
      }

      if (res == '4K' || res == '2160p' || res == '4k') {
        badges.add(buildTextBadge('4K UHD'));
      } else if (res == '1080p' || res == '1080') {
        badges.add(buildTextBadge('1080p FHD'));
      } else if (res == '720p' || res == '720') {
        badges.add(buildTextBadge('720p HD'));
      }

      if (hdr == 'Dolby Vision') {
        badges.add(SvgPicture.asset('assets/images/media_badges/dolby_vision.svg', height: 20, colorFilter: colorFilter));
      } else if (hdr == 'HDR10+') {
        badges.add(buildTextBadge('HDR10+'));
      } else if (hdr.contains('HDR')) {
        badges.add(SvgPicture.asset('assets/images/media_badges/hdr.svg', height: 16, colorFilter: colorFilter));
      } else if (hdr == 'SDR') {
        badges.add(buildTextBadge('SDR'));
      }

      for (String type in audioTypes) {
        if (type == 'Atmos') {
          badges.add(SvgPicture.asset('assets/images/media_badges/dolby_atmos.svg', height: 20, colorFilter: colorFilter));
        } else if (type == 'DD+') {
          badges.add(SvgPicture.asset('assets/images/media_badges/dolby_digital_plus.svg', height: 16, colorFilter: colorFilter));
        } else if (type == 'DD') {
          badges.add(SvgPicture.asset('assets/images/media_badges/dolby_digital.svg', height: 16, colorFilter: colorFilter));
        } else if (type == 'DTS') {
          badges.add(SvgPicture.asset('assets/images/media_badges/dts.svg', height: 16, colorFilter: colorFilter));
        } else if (type == 'AAC') {
          badges.add(buildTextBadge('AAC'));
        }
      }
    } else if (!_isUsingWebview) {
      // Fallback: media_kit
      int w = player.state.width ?? 0;
      int h = player.state.height ?? 0;
      if (_videoTracks.isNotEmpty) {
          final vt = _videoTracks.first;
          w = vt.w ?? w;
          h = vt.h ?? h;
      }
      if (w >= 3840 || h >= 2160) {
        badges.add(buildTextBadge('4K UHD'));
      } else if (w >= 1920 || h >= 1080) {
        badges.add(buildTextBadge('1080p FHD'));
      } else if (w >= 1280 || h >= 720) {
        badges.add(buildTextBadge('720p HD'));
      }
      
      List<String> audioTypes = [];
      for (var at in _audioTracks) {
        String codec = (at.codec ?? '').toUpperCase();
        String type = '';
        if (codec.contains('TRUEHD')) type = 'TrueHD';
        else if (codec.contains('EAC3')) type = 'DD+';
        else if (codec.contains('AC3')) type = 'DD';
        else if (codec.contains('DTS')) type = 'DTS';
        else if (codec.contains('AAC')) type = 'AAC';
        
        if (type.isNotEmpty && !audioTypes.contains(type)) {
          audioTypes.add(type);
        }
      }
      
      for (String type in audioTypes) {
        if (type == 'TrueHD') {
          badges.add(buildTextBadge('TrueHD')); 
        } else if (type == 'DD+') {
          badges.add(SvgPicture.asset('assets/images/media_badges/dolby_digital_plus.svg', height: 16, colorFilter: colorFilter));
        } else if (type == 'DD') {
          badges.add(SvgPicture.asset('assets/images/media_badges/dolby_digital.svg', height: 16, colorFilter: colorFilter));
        } else if (type == 'DTS') {
          badges.add(SvgPicture.asset('assets/images/media_badges/dts.svg', height: 16, colorFilter: colorFilter));
        } else if (type == 'AAC') {
          badges.add(buildTextBadge('AAC'));
        }
      }
    }

    if (badges.isEmpty) return const SizedBox();

    return _buildInfoBadgesRow('', badges);
  }
"""

lines = lines[:start_idx] + [new_code] + lines[end_idx+1:]
with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Patched successfully!")
