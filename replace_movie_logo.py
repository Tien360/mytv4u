with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Pattern for the old container
old_container = """                                                    Container(
                                                      constraints: const BoxConstraints(maxHeight: 120, maxWidth: 500),
                                                      alignment: Alignment.centerLeft,
                                                      margin: EdgeInsets.only(bottom: showMainTitle ? 12 : 8),
                                                      child: Stack(
                                                        alignment: Alignment.centerLeft,
                                                        children: [
                                                          ImageFiltered(
                                                            imageFilter: ImageFilter.blur(sigmaX: 3.0, sigmaY: 3.0),
                                                            child: Image.network(
                                                              _tmdbLogoInfo!.url!,
                                                              fit: BoxFit.contain,
                                                              alignment: Alignment.centerLeft,
                                                              color: Colors.white.withOpacity(0.7),
                                                              errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                            ),
                                                          ),
                                                          Transform.translate(
                                                            offset: const Offset(2, 3),
                                                            child: Image.network(
                                                              _tmdbLogoInfo!.url!,
                                                              fit: BoxFit.contain,
                                                              alignment: Alignment.centerLeft,
                                                              color: Colors.black.withOpacity(0.8),
                                                              errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                            ),
                                                          ),
                                                          Image.network(
                                                            _tmdbLogoInfo!.url!,
                                                            fit: BoxFit.contain,
                                                            alignment: Alignment.centerLeft,
                                                            errorBuilder: (context, error, stackTrace) => const SizedBox(),
                                                          ),
                                                        ],
                                                      ),
                                                    ),"""

new_widget = """                                                    AnimatedMovieLogoWidget(
                                                      logoUrl: _tmdbLogoInfo!.url!,
                                                      showMainTitle: showMainTitle,
                                                    ),"""

if old_container in text:
    text = text.replace(old_container, new_widget)
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Replaced Container with AnimatedMovieLogoWidget!")
else:
    print("Could not find old container!")
