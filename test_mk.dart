import 'package:media_kit/media_kit.dart';
void main() {
  MediaKit.ensureInitialized();
  final player = Player();
  print(player.platform);
}
