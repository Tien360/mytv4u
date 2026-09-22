void main() {
  final url = "premium://play/8M6NIBQJ5VQP";
  final uri = Uri.tryParse(url);
  String rawId = uri != null && uri.pathSegments.isNotEmpty ? uri.pathSegments.last : '';
  print("rawId: '$rawId'");
}
