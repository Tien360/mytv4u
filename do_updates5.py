with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

dir_start = -1
dir_end = -1
for i, line in enumerate(lines):
    if "_movie!.directors.isNotEmpty" in line:
        dir_start = i
    if dir_start != -1 and i > dir_start and "_buildRichText(" in line:
        for j in range(i, i+15):
            if "]," in lines[j]:
                dir_end = j
                break
        break

if dir_start != -1 and dir_end != -1:
    lines = lines[:dir_start] + lines[dir_end+1:]
    print("Removed directors block!")

desc_start = -1
desc_end = -1
for i, line in enumerate(lines):
    if "SelectableText(" in line and i+1 < len(lines) and "_movie!.description.replaceAll(" in lines[i+1]:
        desc_start = i
    if desc_start != -1 and i > desc_start and "height: 1.6," in line:
        for j in range(i, i+10):
            if ")," in lines[j] and j == i+2: # `),` is 2 lines after `height: 1.6,`
                desc_end = j
                break
        if desc_end == -1:
             for j in range(i, i+10):
                 if ")," in lines[j]:
                     desc_end = j
                     break
        break
if desc_start != -1 and desc_end != -1:
    lines = lines[:desc_start] + ["""
                                          Text(
                                            L10n.t('overview') ?? 'Nội dung phim',
                                            style: const TextStyle(
                                              color: Colors.white,
                                              fontWeight: FontWeight.bold,
                                              fontSize: 18,
                                            ),
                                          ),
                                          const SizedBox(height: 12),
                                          SelectableText(
                                            (L10n.currentLang == 'en' && _tmdbDetails != null && _tmdbDetails!['overview'] != null && _tmdbDetails!['overview'].toString().isNotEmpty) 
                                                ? _tmdbDetails!['overview'] 
                                                : _movie!.description.replaceAll(
                                                    RegExp(r'<[^>]*>|&[^;]+;'),
                                                    '',
                                                  ),
                                            style: TextStyle(
                                              fontSize: 15,
                                              color: Colors.white.withValues(alpha: 0.8),
                                              height: 1.6,
                                            ),
                                          ),
"""] + lines[desc_end+1:]
    print("Updated description logic!")


with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.writelines(lines)

