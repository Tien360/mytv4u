import 'package:mytv4u_flutter/api/motchill_scraper.dart';
void main() async {
  final servers = await MotchillScraper.getEpisodeServers('motchill://https://motchillv.co/phim/tho-san-quai-vat-dong-mau-khoi-nguon/tap-1');
  for (var s in servers) {
    print(s['name']);
    print(s['link']);
  }
}
