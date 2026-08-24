import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

directors_ui = """
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
"""

# Find the exact pattern at the end of the actors block
pattern = r"(\}\)\.toList\(\),\s*\),\s*\]\,\s*\),\s*\),\s*\]\,\s*\),)"
if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, lambda m: directors_ui + m.group(1), content, count=1, flags=re.DOTALL)
else:
    print("Pattern not found for adding directors!")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Added directors back")
