import 'package:youtube_explode_dart/youtube_explode_dart.dart';

void main() async {
  var yt = YoutubeExplode();
  try {
    var manifest = await yt.videos.streamsClient.getManifest('0cB5SdPbwtc');
    print('Audio streams: ${manifest.audioOnly.length}');
    print('Video streams: ${manifest.videoOnly.length}');
    print('Muxed streams: ${manifest.muxed.length}');
    if (manifest.muxed.isNotEmpty) {
      print('URL: ${manifest.muxed.first.url}');
    }
  } catch (e) {
    print('Error: $e');
  } finally {
    yt.close();
  }
}
