import re

with open("lib/api/premium_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add _medataDomain variable
if "_medataDomain" not in content:
    content = content.replace("static String? _apiDomain;", "static String? _apiDomain;\n  static String? _medataDomain;")

# Add logic to fetch _medataDomain in _initCache
fetch_logic = """
      if (_medataDomain == null) {
        try {
          final req = http.Request('GET', Uri.parse('https://rip.cryboiz.workers.dev/go/medata'))..followRedirects = false;
          req.headers['User-Agent'] = 'Dart/3.12 (dart:io)';
          final res = await req.send();
          if (res.statusCode == 301 || res.statusCode == 302) {
            final loc = res.headers['location'];
            if (loc != null && loc.isNotEmpty) {
              _medataDomain = loc.endsWith('/') ? loc.substring(0, loc.length - 1) : loc;
            }
          }
        } catch (_) {}
      }
"""

if "_medataDomain == null" not in content:
    content = content.replace("if (_apiDomain == null) {", fetch_logic + "\n      if (_apiDomain == null) {")

# Add a getter
if "static String? get medataDomain => _medataDomain;" not in content:
    content = content.replace("static String? get apiDomain => _apiDomain;", "static String? get apiDomain => _apiDomain;\n  static String? get medataDomain => _medataDomain;")

# Also export ensureInit() to make sure domains are fetched
if "static Future<void> ensureInit() async {" not in content:
    content = content.replace("static Future<void> clearCache() async {", "static Future<void> ensureInit() async {\n    await _initCache();\n  }\n\n  static Future<void> clearCache() async {")

with open("lib/api/premium_api.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated PremiumApi to cache _medataDomain")
