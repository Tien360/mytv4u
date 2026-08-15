import 'package:flutter_test/flutter_test.dart';
import 'package:mytv4u_flutter/api/phim_api.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  test('fetch phim-le', () async {
    SharedPreferences.setMockInitialValues({'enabled_sources': ['ophim']});
    var list = await PhimApi.getMoviesByCategory('phim-le');
    print('phim-le ophim length: \${list.length}');
  });
}
