void main() {
  String _slugify(String text) {
    String lower = text.toLowerCase().trim();
    lower = lower.replaceAll(RegExp(r'[^a-z0-9\s]'), '');
    return lower.replaceAll(RegExp(r'\s+'), '-');
  }
  print(_slugify('Minions & Monsters'));
}
