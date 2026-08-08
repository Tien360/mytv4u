import 'package:youtube_explode_dart/youtube_explode_dart.dart';

void main() async {
  var yt = YoutubeExplode();
  // Venom The Last Dance trailer
  var manifest = await yt.videos.streamsClient.getManifest('__2ABJjxzNo');
  
  var muxedStreams = manifest.muxed.sortByVideoQuality();
  print('Muxed:');
  for (var s in muxedStreams) {
    print('${s.videoResolution} - ${s.url}');
  }
  
  yt.close();
}
