import 'package:mytv4u_flutter/api/phim_api.dart';
import 'package:flutter/widgets.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  try {
    var list = await PhimApi.getMoviesByCategory('phim-le');
    print('phim-le: ' + list.length.toString());
  } catch(e) {
    print('Error: \$e');
  }
}
