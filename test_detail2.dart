import 'dart:async';
import 'package:flutter/widgets.dart';
import 'lib/api/phim_api.dart';
import 'lib/models/movie.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({'enabled_sources': ['premium', 'nguonc', 'kkphim', 'vsmov', 'phim4k', 'free1', 'motchill']});
  
  print('Fetching details for "cho-hoang-va-xuong"...');
  
  PhimApi.fetchMovieDetailStream('cho-hoang-va-xuong').listen((Movie movie) {
    print('--- Update Received ---');
    print('Movie: ${movie.name}');
    print('Source: ${movie.source}');
    print('Servers:');
    for (var srv in movie.episodes) {
      print('  - ${srv.serverName} (${srv.items.length} episodes)');
      if (srv.items.isNotEmpty) {
        print('    [0] name: ${srv.items[0].name}, m3u8Url: ${srv.items[0].m3u8Url}');
      }
    }
  }, onDone: () {
    print('--- Stream Done ---');
  });
}
