import 'package:youtube_explode_dart/youtube_explode_dart.dart';

void main() async {
  final yt = YoutubeExplode();
  final url = 'https://www.youtube.com/playlist?list=PLnsrTI5B-0YOE_451Aq8VMMjY_q4b7iQa';
  try {
    print('Testing playlist get...');
    final playlist = await yt.playlists.get(url);
    print('Title: ${playlist.title}');
    final videos = await yt.playlists.getVideos(playlist.id).take(10).toList();
    print('Count: ${videos.length}');
  } catch (e) {
    print('Error: $e');
  }
  yt.close();
}
