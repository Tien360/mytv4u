with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

# find exact index for the end of MouseRegion(actor) which is `                                              );` before 1786.
# and exact index for `                              const SizedBox(height: 60),` which is around 1871.

start_idx = -1
for i in range(1780, 1790):
    if ");" in lines[i] and "}" not in lines[i]:
        start_idx = i
        break

end_idx = -1
for i in range(1860, 1880):
    if "const SizedBox(height: 60)," in lines[i]:
        end_idx = i
        break

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

new_code = """                                              }).toList(),
                                            ),
                                            if (_directorsTmdb.isNotEmpty) ...[
                                              const SizedBox(height: 32),
                                              Text(
                                                L10n.t('directors') ?? 'Đạo diễn',
                                                style: const TextStyle(
                                                  color: Colors.white,
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: 16,
                                                ),
                                              ),
                                              const SizedBox(height: 16),
                                              Wrap(
                                                spacing: 16,
                                                runSpacing: 16,
                                                children: _directorsTmdb.take(3).map((director) {
                                                  return MouseRegion(
                                                    cursor: SystemMouseCursors.click,
                                                    child: GestureDetector(
                                                      onTap: () {
                                                        if (director['id'] != null && director['id']!.isNotEmpty) {
                                                          _pauseTrailer();
                                                          Navigator.push(
                                                            context,
                                                            MaterialPageRoute(
                                                              builder: (_) => ActorDetailScreen(
                                                                actorId: director['id']!,
                                                                actorName: director['name'] ?? '',
                                                              ),
                                                            ),
                                                          );
                                                        }
                                                      },
                                                      child: Column(
                                                        children: [
                                                          Container(
                                                            width: 60,
                                                            height: 60,
                                                            decoration: BoxDecoration(
                                                              shape: BoxShape.circle,
                                                              border: Border.all(color: Colors.white24),
                                                              color: Colors.white10,
                                                              image: director['profile']!.isNotEmpty
                                                                  ? DecorationImage(
                                                                      image: NetworkImage(director['profile']!),
                                                                      fit: BoxFit.cover,
                                                                    )
                                                                  : null,
                                                            ),
                                                            child: director['profile']!.isEmpty
                                                                ? const Icon(Icons.person, color: Colors.white54)
                                                                : null,
                                                          ),
                                                          const SizedBox(height: 8),
                                                          SizedBox(
                                                            width: 70,
                                                            child: Text(
                                                              director['name'] ?? '',
                                                              textAlign: TextAlign.center,
                                                              maxLines: 2,
                                                              overflow: TextOverflow.ellipsis,
                                                              style: const TextStyle(color: Colors.white, fontSize: 12),
                                                            ),
                                                          ),
                                                        ],
                                                      ),
                                                    ),
                                                  );
                                                }).toList(),
                                              ),
                                            ],
                                          ],
                                        ),
                                      ),
                                  ],
                                ),
"""

if start_idx != -1 and end_idx != -1:
    new_lines = lines[:start_idx + 1] + [new_code] + lines[end_idx:]
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Fixed movie_detail_screen.dart!")
else:
    print("Could not find start or end index!")
