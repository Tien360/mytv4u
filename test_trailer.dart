
import 'dart:io';
import 'package:media_kit/media_kit.dart';

void main() async {
  MediaKit.ensureInitialized();
  final player = Player();
  String options = 'js-runtimes=node';
  (player.platform as dynamic).setProperty('ytdl-format', 'bestvideo[height<=1080]+bestaudio/best');
  (player.platform as dynamic).setProperty('ytdl-raw-options', options);
  
  final url = 'https://www.youtube.com/watch?v=83XGFy-xO3g'; // Silo trailer
  print("Opening url");
  await player.open(Media(url), play: false);
  print("Duration: ${player.state.duration}");
  print("Playing...");
  await player.play();
  await Future.delayed(Duration(seconds: 5));
  print("Duration: ${player.state.duration}");
  print("Position: ${player.state.position}");
  exit(0);
}
