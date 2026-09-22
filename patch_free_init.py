import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

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

# Add await ensureInit() to getRecentMovies, getMoviesByCategory, getMoviesByGenre, getMoviesByCountry, searchMovies, getMovieDetail
funcs_to_patch = ["static Future<List<Movie>> getRecentMovies", "static Future<List<Movie>> getMoviesByCategory", "static Future<List<Movie>> getMoviesByGenre", "static Future<List<Movie>> getMoviesByCountry", "static Future<List<Movie>> searchMovies"]

for func in funcs_to_patch:
    if func in content:
        new_func = func.split(" ")[2] # e.g. getRecentMovies
        content = content.replace(f"{func}(", f"{func}(")
        # Need to inject right after the `{` of the function body
        # Easiest way is to use regex
        
with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Part 1 done")
