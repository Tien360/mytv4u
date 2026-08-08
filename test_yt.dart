import 'package:youtube_explode_dart/youtube_explode_dart.dart';

void main() async {
  var yt = YoutubeExplode();
  var manifest = await yt.videos.streamsClient.getManifest('dQw4w9WgXcQ'); // Rick Astley
  
  var muxedStreams = manifest.muxed.sortByVideoQuality();
  print('Muxed streams sorted by video quality:');
  for (var stream in muxedStreams) {
    print('Resolution: ${stream.videoResolution}, Bitrate: ${stream.bitrate}, Size: ${stream.size}');
  }
  
  var videoOnlyStreams = manifest.videoOnly.sortByVideoQuality();
  print('\nVideo-only streams sorted by video quality:');
  for (var stream in videoOnlyStreams) {
    print('Resolution: ${stream.videoResolution}, Bitrate: ${stream.bitrate}, Size: ${stream.size}');
  }
  
  yt.close();
}
