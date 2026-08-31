import 'dart:io';
void main() async {
  try {
    var result = await Process.run('wmic', ['OS', 'get', 'TotalVisibleMemorySize', '/Value']);
    print(result.stdout);
  } catch (e) {
    print(e);
  }
}
