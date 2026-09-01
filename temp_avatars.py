import io

with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "final directors = crew.where" in line:
        new_lines.append("""    final directors = crew.where((c) => c['job'] == 'Director').toList();
    final writers = crew.where((c) => c['job'] == 'Writer').toList();
    
    final createdBy = widget.mainSeriesDetails['created_by'] as List<dynamic>? ?? [];
    final createdByNames = createdBy.map((c) => c['name']).toSet();
    final validDirectors = directors.where((d) => !createdByNames.contains(d['name'])).toList();
    
    List<Map<String, dynamic>> crewAndGuests = [];
    for (var d in validDirectors) {
      crewAndGuests.add({
        'name': d['name'] ?? '',
        'role': L10n.t('director'),
        'profile_path': d['profile_path'] ?? '',
      });
    }
    for (var w in writers) {
      crewAndGuests.add({
        'name': w['name'] ?? '',
        'role': L10n.t('writer'),
        'profile_path': w['profile_path'] ?? '',
      });
    }
    for (var g in guestStars) {
      crewAndGuests.add({
        'name': g['name'] ?? '',
        'role': g['character'] ?? '',
        'profile_path': g['profile_path'] ?? '',
      });
    }
""")
        skip = True
    elif "return GestureDetector(" in line and skip:
        skip = False
        new_lines.append(line)
    elif not skip:
        new_lines.append(line)

code2 = "".join(new_lines)
# Now replace the rendering logic
start_idx = code2.find("// Crew")
end_idx = code2.find("],", code2.find("},", code2.find("child: ListView.builder("))) + 2

replacement = """// Crew & Guests
                          if (crewAndGuests.isNotEmpty) ...[
                            const SizedBox(height: 16),
                            SizedBox(
                              height: 140,
                              child: ListView.builder(
                                scrollDirection: Axis.horizontal,
                                itemCount: crewAndGuests.length,
                                itemBuilder: (context, idx) {
                                  final person = crewAndGuests[idx];
                                  final profilePath = person['profile_path'];
                                  final profileUrl = TmdbApi.getImageUrl(profilePath);
                                  return Container(
                                    width: 90,
                                    margin: const EdgeInsets.only(right: 12),
                                    child: Column(
                                      children: [
                                        CircleAvatar(
                                          radius: 35,
                                          backgroundColor: Colors.white.withOpacity(0.1),
                                          backgroundImage: profileUrl.isNotEmpty ? NetworkImage(profileUrl) : null,
                                          child: profileUrl.isEmpty ? const Icon(Icons.person, color: Colors.white30) : null,
                                        ),
                                        const SizedBox(height: 8),
                                        Text(
                                          person['name'] ?? '',
                                          textAlign: TextAlign.center,
                                          maxLines: 2,
                                          overflow: TextOverflow.ellipsis,
                                          style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w500),
                                        ),
                                        const SizedBox(height: 2),
                                        Text(
                                          person['role'] ?? '',
                                          textAlign: TextAlign.center,
                                          maxLines: 2,
                                          overflow: TextOverflow.ellipsis,
                                          style: const TextStyle(color: Colors.white54, fontSize: 11),
                                        ),
                                      ],
                                    ),
                                  );
                                },
                              ),
                            ),
                          ],"""

code_final = code2[:start_idx] + replacement + code2[end_idx:]

with open("lib/widgets/air_schedule_dialog.dart", "w", encoding="utf-8") as f:
    f.write(code_final)
print("Updated air_schedule_dialog.dart with unified avatars")
