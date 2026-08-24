with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "if (_tmdbDetails != null) ...[" in line and "status" not in line:
        if i+1 < len(lines) and "status" in lines[i+1]:
            idx = i - 1
            while "SizedBox" in lines[idx] or lines[idx].strip() == "":
                idx -= 1
            # Remove from idx+1 to i-1
            del lines[idx+1:i]
            # Insert exactly one SizedBox
            lines.insert(idx+1, "                                            const SizedBox(height: 24),\n")
            break

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Cleaned up gaps above TMDB block!")
