import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add prints to _fetchPremiumMetadata
old_func = """Future<void> _fetchPremiumMetadata() async {
    if (_movie == null || _isFetchingPremiumMeta) return;"""

new_func = """Future<void> _fetchPremiumMetadata() async {
    print('[_fetchPremiumMetadata] Called!');
    if (_movie == null || _isFetchingPremiumMeta) {
      print('[_fetchPremiumMetadata] Early return: movie == null || isFetching');
      return;
    }"""

content = content.replace(old_func, new_func)

old_checkIds = """final checkIds = premiumEps.where((e) => e['score'] == maxScore).map((e) => e['id'].toString()).take(3).toList();"""
new_checkIds = """final checkIds = premiumEps.where((e) => e['score'] == maxScore).map((e) => e['id'].toString()).take(3).toList();
    print('[_fetchPremiumMetadata] checkIds: $checkIds, medataDomain: ${PremiumApi.medataDomain}');"""

content = content.replace(old_checkIds, new_checkIds)

old_res = """final res = await http.get(
          Uri.parse('${PremiumApi.medataDomain ?? 'https://medata.phim4k.workers.dev'}/?id=$id'),
          headers: {'User-Agent': 'Mozilla/5.0'}
        ).timeout(const Duration(seconds: 4));
        if (res.statusCode == 200) {"""
new_res = """final url = '${PremiumApi.medataDomain ?? 'https://medata.phim4k.workers.dev'}/?id=$id';
        print('[_fetchPremiumMetadata] Fetching: $url');
        final res = await http.get(
          Uri.parse(url),
          headers: {'User-Agent': 'Mozilla/5.0'}
        ).timeout(const Duration(seconds: 4));
        print('[_fetchPremiumMetadata] Response: ${res.statusCode}');
        if (res.statusCode == 200) {"""

content = content.replace(old_res, new_res)

old_setstate = """if (mounted && bestMeta != null) {
      setState(() {"""
new_setstate = """print('[_fetchPremiumMetadata] bestMeta: $bestMeta');
    if (mounted && bestMeta != null) {
      setState(() {"""

content = content.replace(old_setstate, new_setstate)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Injected prints")
