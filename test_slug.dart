void main() {
  String text = 'Minions & Monsters';
  String lower = text.toLowerCase().trim();
  lower = lower.replaceAll(RegExp(r'[^a-z0-9\s]'), '');
  String slug = lower.replaceAll(RegExp(r'\s+'), '-');
  print(slug);
}
