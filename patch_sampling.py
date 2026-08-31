import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the simple logic in _fetchPremiumMetadata
old_logic = """    List<String> ids = [];
    for (var server in _movie!.episodes) {
      if (server.serverName.toLowerCase().contains('premium')) {
        for (var ep in server.items) {
          final uri = Uri.tryParse(ep.m3u8Url);
          if (uri != null && uri.pathSegments.isNotEmpty) {
            ids.add(uri.pathSegments.last);
          }
        }
      }
    }
    
    if (ids.isEmpty) return;
    
    _isFetchingPremiumMeta = true;
    final checkIds = ids.take(3).toList(); // Lấy 3 file đầu để test chất lượng tốt nhất"""

new_logic = """    List<Map<String, dynamic>> premiumEps = [];
    for (var server in _movie!.episodes) {
      if (server.serverName.toLowerCase().contains('premium')) {
        for (var ep in server.items) {
          final uri = Uri.tryParse(ep.m3u8Url);
          if (uri != null && uri.pathSegments.isNotEmpty) {
            // Đánh giá chất lượng từ tên file/server (vd: 2160p, 1080p, 4K)
            String textToSearch = (server.serverName + " " + ep.name).toUpperCase();
            int score = 1;
            if (textToSearch.contains('4K') || textToSearch.contains('2160')) score = 4;
            else if (textToSearch.contains('1080')) score = 3;
            else if (textToSearch.contains('720')) score = 2;
            
            premiumEps.add({
               'id': uri.pathSegments.last,
               'score': score
            });
          }
        }
      }
    }
    
    if (premiumEps.isEmpty) return;
    
    _isFetchingPremiumMeta = true;
    
    // Tìm điểm số cao nhất theo tên
    int maxScore = 1;
    for (var ep in premiumEps) {
      if (ep['score'] > maxScore) maxScore = ep['score'];
    }
    
    // Lấy TẤT CẢ các file có điểm cao nhất (tối đa 3 file) để check API tìm HDR/Audio xịn nhất
    final checkIds = premiumEps.where((e) => e['score'] == maxScore).map((e) => e['id'].toString()).take(3).toList();"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched smart sampling logic")
else:
    print("Could not find old logic to replace")
