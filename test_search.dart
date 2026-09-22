import 'dart:convert';
import 'lib/api/premium_api.dart';

void main() async {
  final res = await PremiumApi.searchMovies('nhat au xuan');
  print('Search result count: ${res['items']?.length}');
  if (res['items'] != null && res['items'].isNotEmpty) {
     final first = res['items'][0];
     print('First item slug: ${first['slug']}');
     final detail = await PremiumApi.getDetail(first['slug']);
     
     final eps = detail['movie']?['episodes'];
     if (eps != null && eps.isNotEmpty) {
        final server = eps[0];
        print('Server name: ${server['server_name']}');
        final items = server['server_data'] ?? server['items'];
        if (items != null && items.isNotEmpty) {
           print('Item 0 link: ${items[0]['link_m3u8']}');
        }
     }
  }
}
