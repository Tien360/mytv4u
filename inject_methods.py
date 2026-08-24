with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

methods = """
  Future<void> _searchAndPlayTmdbMovie(Map<String, dynamic> tmdbMovie) async {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1A1A1A),
        title: Text(L10n.t('searching_movie') ?? 'Đang tìm kiếm phim...', style: const TextStyle(color: Colors.white)),
        content: const SizedBox(height: 50, child: Center(child: CircularProgressIndicator())),
      ),
    );

    try {
      final query = tmdbMovie['title'] ?? tmdbMovie['name'] ?? tmdbMovie['original_title'] ?? tmdbMovie['original_name'];
      final results = await PhimApi.searchMovies(query);
      
      if (mounted) Navigator.pop(context); // Close dialog

      if (results.isNotEmpty) {
        // Try to match year if possible
        final year = (tmdbMovie['release_date'] ?? tmdbMovie['first_air_date'] ?? '').toString().split('-').first;
        var bestMatch = results.first;
        if (year.isNotEmpty) {
           final match = results.where((m) => m.year == year).toList();
           if (match.isNotEmpty) bestMatch = match.first;
        }
        
        if (mounted) {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => MovieDetailScreen(initialMovie: bestMatch),
            ),
          );
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(L10n.t('movie_not_found') ?? 'Rất tiếc, hệ thống chưa cập nhật bộ phim này.'),
              backgroundColor: Colors.redAccent,
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) Navigator.pop(context); // Close dialog
    }
  }

  Widget _buildTmdbHorizontalList(String title, List items) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 32),
        Text(
          title,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
            fontSize: 20,
          ),
        ),
        const SizedBox(height: 16),
        SizedBox(
          height: 220,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: items.length,
            itemBuilder: (context, index) {
              final item = items[index];
              final posterPath = item['poster_path'];
              if (posterPath == null) return const SizedBox();
              
              return Padding(
                padding: const EdgeInsets.only(right: 16),
                child: InkWell(
                  onTap: () => _searchAndPlayTmdbMovie(item),
                  borderRadius: BorderRadius.circular(8),
                  child: SizedBox(
                    width: 120,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: Image.network(
                            'https://image.tmdb.org/t/p/w200$posterPath',
                            height: 180,
                            width: 120,
                            fit: BoxFit.cover,
                            errorBuilder: (c, e, s) => Container(
                              height: 180,
                              width: 120,
                              color: Colors.white10,
                              child: const Icon(Icons.error, color: Colors.white54),
                            ),
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          item['title'] ?? item['name'] ?? '',
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(color: Colors.white70, fontSize: 13),
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
"""

content = content.replace("  Widget _buildRichText(String label, String value) {", methods + "\n  Widget _buildRichText(String label, String value) {")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Injected methods")
