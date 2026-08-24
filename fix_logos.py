import re
with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

old_companies = r"""if \(_tmdbDetails!\['production_companies'\] != null && \(\_tmdbDetails!\['production_companies'\] as List\)\.isNotEmpty\)
\s*_buildRichText\('\$\{L10n\.t\('production_companies'\) \?\? 'Hãng sản xuất'\}: ', \(\_tmdbDetails!\['production_companies'\] as List\)\.map\(\(c\) => c\['name'\]\)\.join\(', '\)\),"""

new_companies = """if (_tmdbDetails!['production_companies'] != null && (_tmdbDetails!['production_companies'] as List).isNotEmpty) ...[
                                              const SizedBox(height: 8),
                                              Text(
                                                '${L10n.t('production_companies') ?? 'Hãng sản xuất'}:',
                                                style: const TextStyle(
                                                  color: Colors.white,
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: 15,
                                                ),
                                              ),
                                              const SizedBox(height: 8),
                                              Wrap(
                                                spacing: 12,
                                                runSpacing: 12,
                                                children: (_tmdbDetails!['production_companies'] as List)
                                                    .where((c) => c['logo_path'] != null)
                                                    .map((c) => Container(
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
                                                        ))
                                                    .toList(),
                                              ),
                                              const SizedBox(height: 8),
                                            ],"""

if re.search(old_companies, content):
    content = re.sub(old_companies, new_companies, content)
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("Logos replaced")
else:
    print("Could not find target")
