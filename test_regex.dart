
void main() {
  String t = 'Hầm SILO - Phần 1';
  t = t.replaceAll(RegExp(r'\(\s*(?:season|phần|part)\s*\d+\s*\)', caseSensitive: false), '');
  t = t.replaceAll(RegExp(r'(?:\s*-\s*)?(?:season|phần|part)\s*\d+', caseSensitive: false), '');
  t = t.replaceAll(RegExp(r'\(\s*\)'), '');
  t = t.replaceAll(RegExp(r'(?:\s*-\s*)?premium', caseSensitive: false), '');
  print('Cleaned: \'' + t.trim() + '\'');
}

