with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

old_code = """                setState(() {
                  _movie = movie;
                  _isLoading = false;
                });
  
                _categorizeServers(movie.episodes);"""

new_code = """                setState(() {
                  _movie = movie;
                  _isLoading = false;
                });
                
                _loadEpisodeProgressAndColor();
  
                _categorizeServers(movie.episodes);"""

c = c.replace(old_code, new_code)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Injected _loadEpisodeProgressAndColor call in _fetchDetail")
