import 'package:http/http.dart' as http;
import 'lib/api/film4k_proxy.dart';

void main() async {
  await Film4kProxy.start();
  
  // Test master m3u8
  String url = Film4kProxy.processUrl('https://film4k.net/api/hls/tiktok/mortal-kombat-ii/master.m3u8');
  print('Requesting: $url');
  
  var res = await http.get(Uri.parse(url));
  print('Master m3u8:\n${res.body}');
  
  // Test v.m3u8
  String vUrl = Film4kProxy.processUrl('https://film4k.net/api/hls/tiktok/mortal-kombat-ii/v.m3u8');
  print('Requesting: $vUrl');
  var resV = await http.get(Uri.parse(vUrl));
  print('v.m3u8 first 500 chars:\n${resV.body.substring(0, 500)}');
}
