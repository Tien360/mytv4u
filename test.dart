void main() {
  final movieName = "Thứ Tư (Phần 1) - Premium TM - Season 02 (Full HD)";
  final movieSeasonMatch = RegExp(r'(?:ph[\u1EA7a]n|m[\u00F9u]a|season|sesion|ss)\s*0*(\d+)', caseSensitive: false).allMatches(movieName);
  if (movieSeasonMatch.isNotEmpty) {
    print("Found: " + movieSeasonMatch.last.group(1)!);
  }
}
