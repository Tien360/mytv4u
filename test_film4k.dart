import 'dart:convert';
import 'package:http/http.dart' as http;
import 'lib/api/film4knet_api.dart';

void main() async {
    final res = await Film4kNetApi.search('minions và quái vật');
    print(res.map((e) => e.name).toList());
}
