with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the Container with AnimatedLogoWidget
old_container = """Container(
                                                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                                            decoration: BoxDecoration(
                                                              color: Colors.white,
                                                              borderRadius: BorderRadius.circular(4),
                                                            ),
                                                            child: Image.network(
                                                              'https://image.tmdb.org/t/p/w200${c['logo_path']}',
                                                              height: 24,
                                                              fit: BoxFit.contain,
                                                            ),
                                                          )"""

new_widget = "AnimatedLogoWidget(logoPath: c['logo_path'])"

if old_container in text:
    text = text.replace(old_container, new_widget)
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Replaced with AnimatedLogoWidget!")
else:
    print("Could not find old container!")
