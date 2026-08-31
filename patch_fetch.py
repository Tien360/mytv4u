import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

helper = """
  Map<String, String> _parseQualityFromFilename(String fn) {
    fn = fn.toUpperCase();
    String res = '';
    if (fn.contains('2160') || fn.contains('4K') || fn.contains('UHD')) res = '4K';
    else if (fn.contains('1080')) res = '1080P';
    else if (fn.contains('720')) res = '720P';

    String hdr = '';
    if (fn.contains('.DV.') || fn.contains('DOLBY VISION') || fn.contains('DOLBY.VISION')) hdr = 'Dolby Vision';
    else if (fn.contains('HDR10+') || fn.contains('HDR10PLUS')) hdr = 'HDR10+';
    else if (fn.contains('HDR10')) hdr = 'HDR10';
    else if (fn.contains('.HDR.') || fn.contains(' HDR ')) hdr = 'HDR';

    String audio = '';
    if (fn.contains('ATMOS')) audio = 'Atmos';
    else if (fn.contains('TRUEHD') || fn.contains('TRUE.HD')) audio = 'TrueHD';
    else if (fn.contains('DTS-HD') || fn.contains('DTS.HD')) audio = 'DTS-HD';
    else if (fn.contains('DTS')) audio = 'DTS';
    else if (fn.contains('DDP') || fn.contains('DD+') || fn.contains('EAC3')) audio = 'DD+';
    else if (fn.contains(' AC3') || fn.contains('.AC3') || fn.contains('DD5.1')) audio = 'DD';
    else if (fn.contains('AAC')) audio = 'AAC';

    return {'resolution': res, 'hdr': hdr, 'audio': audio};
  }
"""

# Insert helper before _fetchPremiumMetadata
content = content.replace("Future<void> _fetchPremiumMetadata() async {", helper + "\n  Future<void> _fetchPremiumMetadata() async {")

old_fetch = """_isFetchingPremiumMeta = true;
    
    // Tìm điểm số cao nhất theo tên
    int maxScore = 1;
    for (var ep in premiumEps) {
      if (ep['score'] > maxScore) maxScore = ep['score'];
    }
    
    // Lấy TẤT CẢ các file có điểm cao nhất (tối đa 3 file) để check API tìm HDR/Audio xịn nhất
    final checkIds = premiumEps.where((e) => e['score'] == maxScore).map((e) => e['id'].toString()).take(3).toList();
    Map<String, dynamic>? bestMeta;
    int bestScore = -1;
    
    for (var ep in premiumEps.where((e) => e['score'] == maxScore).take(3)) {
      var id = ep['id'].toString();
      try {
        final res = await http.get(
          Uri.parse('https://medata.phim4k.workers.dev/?id=$id'),
        ).timeout(const Duration(seconds: 10));
        
        if (res.statusCode == 200) {
          final data = json.decode(res.body);
          
          int score = 0;
          String resText = (data['resolution'] ?? '').toString();
          if (resText.contains('4K') || resText.contains('2160')) score += 100;
          else if (resText.contains('1080')) score += 50;
          
          String hdr = (data['hdr'] ?? '').toString();
          if (hdr == 'Dolby Vision') score += 20;
          else if (hdr.contains('HDR')) score += 10;
          
          if (score > bestScore) {
            bestScore = score;
            bestMeta = data;
            bestMeta!['fallback_filename'] = ep['filename'];
          }
        }
      } catch (e) {}
    }
    
    if (mounted && bestMeta != null) {
      setState(() {
        _premiumMetadata = bestMeta;
      });
    }"""

new_fetch = """_isFetchingPremiumMeta = true;
    
    // 1. Dò nhanh từ tên file xem có đủ info không (Fast Path Bypass)
    Map<String, dynamic>? bestMeta;
    int bestRichScore = -1;
    
    for (var ep in premiumEps) {
      String fn = ep['filename'].toString();
      if (fn.isNotEmpty) {
        var q = _parseQualityFromFilename(fn);
        int richScore = ep['score'] * 100; // Resolution base score (400, 300...)
        if (q['hdr']!.isNotEmpty) richScore += 50;
        if (q['audio']!.isNotEmpty) richScore += 50;
        
        // Nếu tên file mô tả chi tiết cả chất lượng lẫn HDR hoặc Audio, ta ưu tiên xài luôn
        if (richScore > bestRichScore && (q['hdr']!.isNotEmpty || q['audio']!.isNotEmpty)) {
          bestRichScore = richScore;
          bestMeta = {
             'resolution': q['resolution'],
             'hdr': q['hdr'],
             'audioTracks': [{'codec': q['audio']}],
             'fallback_filename': fn
          };
        }
      }
    }
    
    // Nếu tìm thấy file có ghi rành rành HDR / DV, không cần gọi API
    if (bestMeta != null) {
      if (mounted) {
        setState(() {
          _premiumMetadata = bestMeta;
        });
      }
      return;
    }

    // 2. Nếu tên file không ghi gì (ví dụ: Tập 1.mkv) -> Phải gọi API
    int maxScore = 1;
    for (var ep in premiumEps) {
      if (ep['score'] > maxScore) maxScore = ep['score'];
    }
    
    bestScore = -1;
    for (var ep in premiumEps.where((e) => e['score'] == maxScore).take(3)) {
      var id = ep['id'].toString();
      try {
        final res = await http.get(
          Uri.parse('https://medata.phim4k.workers.dev/?id=$id'),
        ).timeout(const Duration(seconds: 10));
        
        if (res.statusCode == 200) {
          final data = json.decode(res.body);
          
          int score = 0;
          String resText = (data['resolution'] ?? '').toString();
          if (resText.contains('4K') || resText.contains('2160')) score += 100;
          else if (resText.contains('1080')) score += 50;
          
          String hdr = (data['hdr'] ?? '').toString();
          if (hdr == 'Dolby Vision') score += 20;
          else if (hdr.contains('HDR')) score += 10;
          
          if (score > bestScore) {
            bestScore = score;
            bestMeta = data;
            bestMeta!['fallback_filename'] = ep['filename'];
          }
        }
      } catch (e) {}
    }
    
    if (mounted && bestMeta != null) {
      setState(() {
        _premiumMetadata = bestMeta;
      });
    }"""

content = content.replace(old_fetch, new_fetch)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated fast path parsing")
