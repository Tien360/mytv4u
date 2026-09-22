void main() {
  final uri = Uri.parse('premium://file/8M6NIBQJ5VQP');
  print('Host: ${uri.host}');
  print('Path segments: ${uri.pathSegments}');
}
