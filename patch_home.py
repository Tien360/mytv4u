import re

with open('lib/screens/home_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add _heroLogos map
content = content.replace("List<Movie> _heroMovies = [];", "List<Movie> _heroMovies = [];\n  Map<String, String> _heroLogos = {};")

# 2. Add fetching logos in the loop
target_loop = """        // Fetch backdrops for movies from TMDB for better quality
        for (int i = 0; i < selected.length; i++) {
          final m = selected[i];
          final isTvSeries = m.episodes.isNotEmpty && m.episodes.first.items.length > 1;
          final backdrop = await PhimApi.getMovieTmdbBackdrop(m.name, m.originalName, m.year, isTvSeries);
          if (mounted && backdrop != null && backdrop.isNotEmpty) {
            setState(() {
              _heroMovies[i].posterUrl = backdrop;
            });
          }
        }"""
replacement_loop = """        // Fetch backdrops for movies from TMDB for better quality
        for (int i = 0; i < selected.length; i++) {
          final m = selected[i];
          final isTvSeries = m.episodes.isNotEmpty && m.episodes.first.items.length > 1;
          final backdrop = await PhimApi.getMovieTmdbBackdrop(m.name, m.originalName, m.year, isTvSeries);
          if (mounted && backdrop != null && backdrop.isNotEmpty) {
            setState(() {
              _heroMovies[i].posterUrl = backdrop;
            });
          }
          final logoUrl = await PhimApi.getMovieTmdbLogo(m.name, m.originalName, m.year, isTvSeries, L10n.currentLang);
          if (mounted && logoUrl != null) {
            setState(() {
              _heroLogos[m.slug] = logoUrl;
            });
          }
        }"""
content = content.replace(target_loop, replacement_loop)

# 3. Add key to Center inside AnimatedSwitcher
target_center = """            child: Center(
              child: ConstrainedBox("""
replacement_center = """            child: Center(
              key: ValueKey<int>(_currentHeroIndex),
              child: ConstrainedBox("""
content = content.replace(target_center, replacement_center)

# 4. Wrap the Container with GestureDetector to make the whole banner clickable, remove the Play button, and change Title to Logo
target_banner = """              child: Stack(
                fit: StackFit.expand,
                children: ["""
replacement_banner = """              child: GestureDetector(
                onTap: () => _navigateToDetail(_heroMovies[_currentHeroIndex], 'banner_${_heroMovies[_currentHeroIndex].slug}'),
                child: MouseRegion(
                  cursor: SystemMouseCursors.click,
                  child: Stack(
                    fit: StackFit.expand,
                    children: ["""
content = content.replace(target_banner, replacement_banner)

target_close_banner = """                        ),
                      ),
                    ),
                  ),
                  
                  // Thumbnails"""
replacement_close_banner = """                        ),
                      ),
                    ),
                  ),
                  ), // end MouseRegion
                ), // end GestureDetector
                  
                  // Thumbnails"""
content = content.replace(target_close_banner, replacement_close_banner)

with open('lib/screens/home_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Applied Python Script 1")
