
void main() {
  String t = 'Silo (Season 1)';
  t = t.replaceAll(RegExp(r'\(\s*(?:season|ph?n|part)\s*\d+\s*\)', caseSensitive: false), '');
  print('Cleaned: \'' + t.trim() + '\'');
}

