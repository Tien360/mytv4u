import 'dart:io';

void main() {
  final file = File('lib/screens/player_screen.dart');
  var content = file.readAsStringSync();
  print('Start patching player_screen.dart');
}
