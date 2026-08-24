import re

with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("Map<String, String> _heroLogos = {};", "Map<String, TmdbLogoInfo> _heroLogos = {};")

content = re.sub(
    r"_heroLogos\[movie\.slug\]\s*=\s*logoInfo\.logoUrl!;",
    r"_heroLogos[movie.slug] = logoInfo;",
    content
)

content = re.sub(
    r"Timer\.periodic\(const Duration\(seconds: 8\),",
    r"Timer.periodic(const Duration(seconds: 15),",
    content
)

# Replace the Title / Logo block
# Find where it starts and where it ends
start_marker = "// Title / Logo"
end_marker = "const SizedBox(height: 12),"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker, idx_start)

if idx_start != -1 and idx_end != -1:
    new_block = """// Title / Logo
                                      Builder(
                                          builder: (context) {
                                            final currentHero = _heroMovies[_currentHeroIndex];
                                            final logoInfo = _heroLogos[currentHero.slug];
                                            String mainTitle = currentHero.name;
                                            String subTitle = currentHero.originalName;
                                            
                                            if (logoInfo != null && logoInfo.logoUrl != null) {
                                              final bool isDarkLogo = logoInfo.brightness != null && logoInfo.brightness! < 128;
                                              return Container(
                                                constraints: const BoxConstraints(
                                                  maxHeight: 120,
                                                  maxWidth: 400,
                                                ),
                                                alignment: Alignment.centerLeft,
                                                child: Stack(
                                                  alignment: Alignment.centerLeft,
                                                  children: [
                                                    if (isDarkLogo)
                                                      Positioned.fill(
                                                        child: ImageFiltered(
                                                          imageFilter: ImageFilter.blur(sigmaX: 3.0, sigmaY: 3.0),
                                                          child: Image.network(
                                                            logoInfo.logoUrl!,
                                                            fit: BoxFit.contain,
                                                            alignment: Alignment.centerLeft,
                                                            color: Colors.white.withOpacity(0.5),
                                                          ),
                                                        ),
                                                      ),
                                                    Image.network(
                                                      logoInfo.logoUrl!,
                                                      fit: BoxFit.contain,
                                                      alignment: Alignment.centerLeft,
                                                      errorBuilder: (context, error, stackTrace) {
                                                        return Text(
                                                          currentHero.displayName,
                                                          style: const TextStyle(
                                                            color: Colors.white,
                                                            fontSize: 40,
                                                            fontWeight: FontWeight.bold,
                                                            height: 1.1,
                                                          ),
                                                        );
                                                      },
                                                    ),
                                                  ],
                                                ),
                                              );
                                            } else {
                                              return Column(
                                                crossAxisAlignment: CrossAxisAlignment.start,
                                                children: [
                                                  Text(
                                                    mainTitle,
                                                    style: const TextStyle(
                                                      color: Colors.white,
                                                      fontSize: 40,
                                                      fontWeight: FontWeight.bold,
                                                      height: 1.1,
                                                      shadows: [Shadow(color: Colors.black87, blurRadius: 10)],
                                                    ),
                                                  ),
                                                  if (subTitle.isNotEmpty && subTitle != mainTitle) ...[
                                                    const SizedBox(height: 4),
                                                    Text(
                                                      subTitle,
                                                      style: const TextStyle(
                                                        color: Colors.white70,
                                                        fontSize: 20,
                                                        fontWeight: FontWeight.w500,
                                                        shadows: [Shadow(color: Colors.black87, blurRadius: 6)],
                                                      ),
                                                    ),
                                                  ]
                                                ],
                                              );
                                            }
                                          },
                                      ),
                                      """
    content = content[:idx_start] + new_block + content[idx_end:]

with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
