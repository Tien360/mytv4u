import re

with open("lib/api/premium_resolver.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add _dynamicBaseDomain and _getDynamicBaseDomain
dynamic_domain_func = """
  static String? _dynamicBaseDomain;

  static Future<String?> _getDynamicBaseDomain() async {
    if (_dynamicBaseDomain != null) return _dynamicBaseDomain;
    try {
      final client = http.Client();
      final request = http.Request('GET', Uri.parse('https://rip.cryboiz.workers.dev/go/cdn'))
        ..followRedirects = false;
      final response = await client.send(request).timeout(const Duration(seconds: 5));
      
      String? location;
      if (response.statusCode == 301 || response.statusCode == 302 || response.statusCode == 307 || response.statusCode == 308) {
         location = response.headers['location'];
      }
      
      if (location != null && location.isNotEmpty) {
        final uri = Uri.parse(location);
        final host = uri.host;
        final parts = host.split('.');
        if (parts.length > 2) {
          _dynamicBaseDomain = parts.sublist(1).join('.');
          print('[PremiumResolver] Dynamic CDN Base Domain: $_dynamicBaseDomain');
          return _dynamicBaseDomain;
        }
      }
    } catch (e) {
      print('[PremiumResolver] Error fetching dynamic CDN: $e');
    }
    return null;
  }

  static Future<DateTime> _getUtcTime() async {"""

content = content.replace("  static Future<DateTime> _getUtcTime() async {", dynamic_domain_func)

# Inject dynamic domain usage in getVideoStream
old_loop_start = """    List<String> streams = [];
    for (var server in _servers) {"""

new_loop_start = """    final dynamicBase = await _getDynamicBaseDomain();
    
    List<String> streams = [];
    for (var server in _servers) {"""

content = content.replace(old_loop_start, new_loop_start)

# Inject cdn replacement
old_cdn = """        final secret = server['secret']!;
        final cdn = server['cdn']!;
        final ua = server['ua']!;"""

new_cdn = """        final secret = server['secret']!;
        String cdn = server['cdn']!;
        if (dynamicBase != null) {
          final uri = Uri.parse(cdn);
          final svPrefix = uri.host.split('.').first;
          cdn = "${uri.scheme}://$svPrefix.$dynamicBase";
        }
        final ua = server['ua']!;"""

content = content.replace(old_cdn, new_cdn)

with open("lib/api/premium_resolver.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched successfully.")
