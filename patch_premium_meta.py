import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add state variables
state_pattern = re.compile(r"(class _MovieDetailScreenState extends State<MovieDetailScreen> \{\s+)(Movie\? _movie;)")
state_new = r"\1Map<String, dynamic>? _premiumMetadata;\n  bool _isFetchingPremiumMeta = false;\n  \2"
content = state_pattern.sub(state_new, content)

# 2. Add _fetchPremiumMetadata method before _fetchDetail
method_str = """
  Future<void> _fetchPremiumMetadata() async {
    if (_movie == null || _isFetchingPremiumMeta) return;
    
    List<String> ids = [];
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
    final checkIds = ids.take(3).toList(); // Lấy 3 file đầu để test chất lượng tốt nhất
    Map<String, dynamic>? bestMeta;
    int bestScore = -1;
    
    for (var id in checkIds) {
      try {
        final res = await http.get(
          Uri.parse('https://medata.phim4k.workers.dev/?id=$id'),
          headers: {'User-Agent': 'Mozilla/5.0'}
        ).timeout(const Duration(seconds: 4));
        if (res.statusCode == 200) {
          final data = json.decode(res.body);
          final resStr = (data['resolution'] ?? '').toString().toUpperCase();
          int score = 1;
          if (resStr.contains('4K') || resStr.contains('2160')) score = 4;
          else if (resStr.contains('1080')) score = 3;
          else if (resStr.contains('720')) score = 2;
          
          if (score > bestScore) {
            bestScore = score;
            bestMeta = data;
          }
        }
      } catch (e) {}
    }
    
    if (mounted && bestMeta != null) {
      setState(() {
        _premiumMetadata = bestMeta;
      });
    }
  }

  void _fetchDetail() {"""
content = content.replace("void _fetchDetail() {", method_str)

# 3. Call _fetchPremiumMetadata in _fetchDetail listener
call_pattern = re.compile(r"(_fetchTmdbLogo\(movie\);\s+// Bắt đầu timer)")
call_new = r"_fetchPremiumMetadata();\n                \1"
content = call_pattern.sub(call_new, content)

# 4. Add the badges to the UI. Since I removed the HD badge previously, I will put it right before _getAgeRating
badge_pattern = re.compile(r"(if \(_getAgeRating\(\) != null\)\s+_buildBadge\(\s+_getAgeRating\(\)!,\s+\['R', 'NC-17', 'TV-MA', '18\+'\]\.contains\(_getAgeRating\(\)\) \? Colors\.redAccent : Colors\.orangeAccent,\s+\),)")
badge_new = """if (_premiumMetadata != null) ...[
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
                                                ),
                                              \1"""
content = badge_pattern.sub(badge_new, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added premium metadata feature!")
