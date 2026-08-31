import 'package:youtube_explode_dart/youtube_explode_dart.dart';

void main() async {
  var yt = YoutubeExplode();
  try {
    var playlist = await yt.playlists.get('RD0cB5SdPbwtc');
    print('Title: ${playlist.title}');
    int count = 0;
    await for (var video in yt.playlists.getVideos(playlist.id)) {
      print('Video: ${video.title} (${video.id})');
      count++;
      if (count > 5) break;
    }
  } catch (e) {
    print('Error: $e');
  } finally {
    yt.close();
  }
}
