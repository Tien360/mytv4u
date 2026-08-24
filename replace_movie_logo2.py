import re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

pattern = r"Container\(\s*constraints: const BoxConstraints\(maxHeight: 120, maxWidth: 500\),\s*alignment: Alignment\.centerLeft,\s*margin: EdgeInsets\.only\(bottom: showMainTitle \? 12 : 8\),\s*child: Stack\(\s*alignment: Alignment\.centerLeft,\s*children: \[\s*ImageFiltered\(\s*imageFilter: ImageFilter\.blur\(sigmaX: 3\.0, sigmaY: 3\.0\),\s*child: Image\.network\(\s*_tmdbLogoInfo!\.url!,\s*fit: BoxFit\.contain,\s*alignment: Alignment\.centerLeft,\s*color: Colors\.white\.withOpacity\(0\.7\),\s*errorBuilder: \(context, error, stackTrace\) => const SizedBox\(\),\s*\),\s*\),\s*Transform\.translate\(\s*offset: const Offset\(2, 3\),\s*child: Image\.network\(\s*_tmdbLogoInfo!\.url!,\s*fit: BoxFit\.contain,\s*alignment: Alignment\.centerLeft,\s*color: Colors\.black\.withOpacity\(0\.8\),\s*errorBuilder: \(context, error, stackTrace\) => const SizedBox\(\),\s*\),\s*\),\s*Image\.network\(\s*_tmdbLogoInfo!\.url!,\s*fit: BoxFit\.contain,\s*alignment: Alignment\.centerLeft,\s*errorBuilder: \(context, error, stackTrace\) => const SizedBox\(\),\s*\),\s*\],\s*\),\s*\)"

new_widget = "AnimatedMovieLogoWidget(logoUrl: _tmdbLogoInfo!.url!, showMainTitle: showMainTitle)"

if re.search(pattern, text):
    text = re.sub(pattern, new_widget, text)
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Replaced Container with AnimatedMovieLogoWidget!")
else:
    print("Could not find pattern!")
