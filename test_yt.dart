
import 'package:youtube_explode_dart/youtube_explode_dart.dart';

void main() async {
  var yt = YoutubeExplode();
  try {
    var manifest = await yt.videos.streamsClient.getManifest('83XGFy-xO3g');
    var streamInfo = manifest.muxed.withHighestBitrate();
    print("URL: ${streamInfo.url}");
  } catch (e) {
    print("Error: $e");
  } finally {
    yt.close();
  }
}
