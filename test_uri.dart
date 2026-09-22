void main() {
  final uri = Uri.parse('premium://8M6NIBQJ5VQP');
  print('Host: ${uri.host}');
  print('Path: ${uri.path}');
  print('Path segments: ${uri.pathSegments}');
}
