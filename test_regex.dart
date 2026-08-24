void main() {
  List<String> names = [
    'Mikael: Thợ Săn Hai Thế Giới (2026) Mikael: Pemburu Dua Alam',
    'Batman (2022)',
    'Spider Man 3 Vietsub Thuyết Minh HD'
  ];
  
  for (String name in names) {
    String parsedName = name;
    String parsedOriginalName = 'Original';
    String parsedYear = '';
    
    final regex = RegExp(r'^(.*?)\s*\((\d{4})\)\s*(.*)$');
    final match = regex.firstMatch(parsedName);
    if (match != null) {
      parsedName = match.group(1)?.trim() ?? parsedName;
      String extractedYear = match.group(2) ?? '';
      if (parsedYear.isEmpty && extractedYear.isNotEmpty) {
        parsedYear = extractedYear;
      }
      String extractedOriginalName = match.group(3)?.trim() ?? '';
      if (extractedOriginalName.isNotEmpty) {
        parsedOriginalName = extractedOriginalName;
      }
    }
    
    print('Name: $name => parsedName: $parsedName, parsedOriginalName: $parsedOriginalName, year: $parsedYear');
  }
}
