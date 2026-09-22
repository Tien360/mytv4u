import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Replace function signatures to include await ensureInit()
replacements = {
    "static Future<List<Movie>> getRecentMovies({int page = 1}) async {": "static Future<List<Movie>> getRecentMovies({int page = 1}) async {\n    await ensureInit();",
    "static Future<List<Movie>> getMoviesByCategory(\n    String slug, {\n    int page = 1,\n  }) async {": "static Future<List<Movie>> getMoviesByCategory(\n    String slug, {\n    int page = 1,\n  }) async {\n    await ensureInit();",
    "static Future<List<Movie>> getMoviesByGenre(\n    String slug, {\n    int page = 1,\n  }) async {": "static Future<List<Movie>> getMoviesByGenre(\n    String slug, {\n    int page = 1,\n  }) async {\n    await ensureInit();",
    "static Future<List<Movie>> getMoviesByCountry(\n    String slug, {\n    int page = 1,\n  }) async {": "static Future<List<Movie>> getMoviesByCountry(\n    String slug, {\n    int page = 1,\n  }) async {\n    await ensureInit();",
    "static Future<List<Movie>> searchMovies(String keyword) async {": "static Future<List<Movie>> searchMovies(String keyword) async {\n    await ensureInit();",
    "static Stream<Movie> getMovieDetail(": "static Stream<Movie> getMovieDetail(" # For stream, it's not async block directly, we should inject into the generator or stream controller. Wait, getMovieDetail returns Stream<Movie>. It has `late StreamController<Movie> controller;`
}

for k, v in replacements.items():
    content = content.replace(k, v)

# For getMovieDetail:
old_getDetail = """  static Stream<Movie> getMovieDetail(
    String slug, {
    Movie? initialMovie,
    List<String> enabledSources = const [
      'kkphim',
      'vsmov',
      'film4knet',
      'free2',
      'free1',
      'motchill',
    ],
  }) {
    late StreamController<Movie> controller;
    bool isClosed = false;

    void startFetching() async {"""

new_getDetail = """  static Stream<Movie> getMovieDetail(
    String slug, {
    Movie? initialMovie,
    List<String> enabledSources = const [
      'kkphim',
      'vsmov',
      'film4knet',
      'free2',
      'free1',
      'motchill',
    ],
  }) {
    late StreamController<Movie> controller;
    bool isClosed = false;

    void startFetching() async {
      await ensureInit();"""

content = content.replace(old_getDetail, new_getDetail)

with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(content)

print("Part 2 done")
