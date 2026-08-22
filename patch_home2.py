import re

with open('lib/screens/home_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace Title
target_title = """                            // Title
                            Text(
                              _heroMovies[_currentHeroIndex].displayName,
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 40, // 2.5rem
                                fontWeight: FontWeight.bold,
                                height: 1.1,
                              ),
                            ),"""
replacement_title = """                            // Title / Logo
                            if (_heroLogos[_heroMovies[_currentHeroIndex].slug] != null)
                              Container(
                                constraints: const BoxConstraints(maxHeight: 120, maxWidth: 400),
                                alignment: Alignment.centerLeft,
                                child: Image.network(
                                  _heroLogos[_heroMovies[_currentHeroIndex].slug]!,
                                  fit: BoxFit.contain,
                                  alignment: Alignment.centerLeft,
                                  errorBuilder: (context, error, stackTrace) {
                                    return Text(
                                      _heroMovies[_currentHeroIndex].displayName,
                                      style: const TextStyle(
                                        color: Colors.white,
                                        fontSize: 40,
                                        fontWeight: FontWeight.bold,
                                        height: 1.1,
                                      ),
                                    );
                                  },
                                ),
                              )
                            else
                              Text(
                                _heroMovies[_currentHeroIndex].displayName,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 40,
                                  fontWeight: FontWeight.bold,
                                  height: 1.1,
                                ),
                              ),"""
content = content.replace(target_title, replacement_title)

# 2. Remove Play button
target_button = """                            const SizedBox(height: 24),
                            // Circular Play Button
                            GestureDetector(
                              onTap: () => _navigateToDetail(_heroMovies[_currentHeroIndex], 'banner_${_heroMovies[_currentHeroIndex].slug}'),
                              child: Container(
                                width: 70,
                                height: 70,
                                decoration: BoxDecoration(
                                  color: Theme.of(context).primaryColor,
                                  shape: BoxShape.circle,
                                  boxShadow: [
                                    BoxShadow(
                                      color: Theme.of(context).primaryColor.withOpacity(0.4),
                                      blurRadius: 15,
                                      offset: const Offset(0, 4),
                                    ),
                                  ],
                                ),
                                child: const Icon(Icons.play_arrow, size: 36, color: Colors.white), 
                              ),
                            ),"""
replacement_button = """                            const SizedBox(height: 16),"""
content = content.replace(target_button, replacement_button)

with open('lib/screens/home_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Applied Python Script 2")
