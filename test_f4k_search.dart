import 'package:http/http.dart' as http;
import 'lib/api/film4knet_api.dart';
import 'lib/models/movie.dart';

void main() async {
    print('Searching...');
    final results = await Film4kNetApi.search('minions');
    for (var m in results) {
        print('Found: \ (\) - slugs: \');
    }
}
