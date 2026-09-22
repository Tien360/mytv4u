import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add import
if "premium_api.dart" not in content:
    content = content.replace("import 'dart:convert';", "import 'dart:convert';\nimport 'premium_api.dart';")

# 2. Replace _fetchPremiumSource
old_fetch_premium_source = """  static Future<List<Movie>> _fetchPremiumSource(String url) async {
    try {
      final res = await http
          .get(Uri.parse(url))
          .timeout(const Duration(seconds: 15));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final items = (data['items'] as List?) ?? [];
        return items.map((e) {
          var map = Map<String, dynamic>.from(e as Map<String, dynamic>);
          final originalSlug = (map['slug'] ?? '')
              .toString(); // save original slug before overriding
          final type = map['type'] == 'series' ? 'series' : 'movie';
          final id = map['raw_payload'] ?? map['_id'];
          if (id != null) {
            map['slug'] = 'premium-$type-$id';
          }
          var m = Movie.fromJson(map, defaultSource: 'premium');
          // Store original slug so detail fetch can use it
          final newSlugs = Map<String, String>.from(m.sourceSlugs);
          newSlugs['premium_original'] = originalSlug;
          return m.copyWith(quality: 'Premium', sourceSlugs: newSlugs);
        }).toList();
      }
    } catch (e) {}
    return [];
  }"""

new_fetch_premium_source = """  static Future<List<Movie>> _fetchPremiumSource(String premiumSuffix) async {
    try {
      // Parse premiumSuffix, e.g. /movies?page=1&filterType=the-loai&filterValue=han-hanh
      final uri = Uri.parse(premiumSuffix);
      final page = int.tryParse(uri.queryParameters['page'] ?? '1') ?? 1;
      final filterType = uri.queryParameters['filterType'] ?? '';
      final filterValue = uri.queryParameters['filterValue'] ?? '';
      
      final data = await PremiumApi.getHomeList(filterType, filterValue, page);
      final items = (data['items'] as List?) ?? [];
      return items.map((e) {
        var map = Map<String, dynamic>.from(e as Map<String, dynamic>);
        final originalSlug = (map['slug'] ?? '').toString();
        final type = map['type'] == 'series' ? 'series' : 'movie';
        final id = map['raw_payload'] ?? map['_id'];
        if (id != null) {
          map['slug'] = 'premium-$type-$id';
        }
        var m = Movie.fromJson(map, defaultSource: 'premium');
        final newSlugs = Map<String, String>.from(m.sourceSlugs);
        newSlugs['premium_original'] = originalSlug;
        return m.copyWith(quality: 'Premium', sourceSlugs: newSlugs);
      }).toList();
    } catch (e) {
      print('[Premium DEBUG] _fetchPremiumSource error: $e');
    }
    return [];
  }"""

content = content.replace(old_fetch_premium_source, new_fetch_premium_source)

# 3. Fix the caller in _fetchAndMerge
content = content.replace(
"""        enabledSources.contains('premium')
            ? _fetchPremiumSource(
                'https://dogtail.oxaliplatin.workers.dev/api/premium$premiumSuffix',
              )
            : Future.value(<Movie>[]),""",
"""        enabledSources.contains('premium')
            ? _fetchPremiumSource(premiumSuffix)
            : Future.value(<Movie>[]),"""
)

with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("phim_api.dart patched part 1")
