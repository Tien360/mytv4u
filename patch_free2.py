import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace all 'phim4k' with 'free2' in variable names and keys
content = content.replace("phim4kUrl", "free2Url")
content = content.replace("_normalizePhim4K", "_normalizeFree2")
content = content.replace("'phim4k'", "'free2'")
content = content.replace("Phim4K", "Free2")
content = content.replace("urlPhim4K", "urlFree2")

# 2. Make URLs dynamic
content = content.replace("static const String free2Url = 'https://free2.phim4k.lol/api';", "static String free2Url = 'https://free2.phim4k.lol/api';")
content = content.replace("static const String free1Url = 'https://free1.p4k.dpdns.org';", "static String free1Url = 'https://free1.p4k.dpdns.org';")
content = content.replace("static const String free1List = 'https://free1.p4k.dpdns.org/danh-sach';", "static String free1List = 'https://free1.p4k.dpdns.org/danh-sach';")

init_func = """  static bool _initialized = false;
  static Future<void> ensureInit() async {
    if (_initialized) return;
    _initialized = true;
    try {
      final req1 = http.Request('GET', Uri.parse('https://rip.cryboiz.workers.dev/go/free1'))..followRedirects = false;
      final res1 = await http.Client().send(req1).timeout(const Duration(seconds: 5));
      if (res1.isRedirect && res1.headers['location'] != null) {
        String loc = res1.headers['location']!;
        if (loc.endsWith('/')) loc = loc.substring(0, loc.length - 1);
        free1Url = loc;
        free1List = '$loc/danh-sach';
      }
    } catch (_) {}
    
    try {
      final req2 = http.Request('GET', Uri.parse('https://rip.cryboiz.workers.dev/go/free2'))..followRedirects = false;
      final res2 = await http.Client().send(req2).timeout(const Duration(seconds: 5));
      if (res2.isRedirect && res2.headers['location'] != null) {
        String loc = res2.headers['location']!;
        if (loc.endsWith('/')) loc = loc.substring(0, loc.length - 1);
        // Ensure /api suffix if not present
        if (!loc.endsWith('/api')) loc = '$loc/api';
        free2Url = loc;
      }
    } catch (_) {}
  }
  
  // --- Normalization functions ---"""

content = content.replace("// --- Normalization functions ---", init_func)

# 3. Add await ensureInit() safely!
# We will use regex substitution to insert it right after the opening brace of the function body.
func_regexes = [
    r"(static Future<List<Movie>> getRecentMovies.*?{)",
    r"(static Future<List<Movie>> getMoviesByCategory.*?{)",
    r"(static Future<List<Movie>> getMoviesByGenre.*?{)",
    r"(static Future<List<Movie>> getMoviesByCountry.*?{)",
    r"(static Future<List<Movie>> searchMovies.*?{)"
]
for reg in func_regexes:
    content = re.sub(reg, r"\1\n    await ensureInit();", content, flags=re.DOTALL)

# For getMovieDetail, we insert it into startFetching
old_startFetching = """    void startFetching() async {"""
new_startFetching = """    void startFetching() async {
      await ensureInit();"""
content = content.replace(old_startFetching, new_startFetching)

with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(content)

print("Patching phim_api done")
