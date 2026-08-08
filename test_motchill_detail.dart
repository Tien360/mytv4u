import 'package:mytv4u_flutter/api/motchill_scraper.dart';
void main() async {
  final movie = await MotchillScraper.getDetail('tho-san-quai-vat-dong-mau-khoi-nguon');
  if (movie == null) {
    print('movie is null');
  } else {
    for (var ep in movie.episodes) {
      print('${ep.serverName}: ${ep.items.length} items');
      print('First item link: ${ep.items.first.m3u8Url}');
    }
  }
}
