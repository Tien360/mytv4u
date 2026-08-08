import 'package:mytv4u_flutter/api/motchill_scraper.dart';
void main() async {
  final m = await MotchillScraper.search('venom');
  if (m.isNotEmpty) {
    final movie = await MotchillScraper.getDetail(m.first.slug);
    if (movie != null) {
      print(movie.episodes.first.items.first.m3u8Url);
    }
  }
}
