import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class LocationHelper {
  static String userCountry = 'VN'; // Mặc định
  static bool _initialized = false;

  static Future<void> initUserCountry() async {
    if (_initialized) return;
    try {
      final prefs = await SharedPreferences.getInstance();
      final cachedCountry = prefs.getString('cached_user_country');
      if (cachedCountry != null && cachedCountry.isNotEmpty) {
        userCountry = cachedCountry;
      }

      final response = await http.get(Uri.parse('http://ip-api.com/json/')).timeout(const Duration(seconds: 3));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['countryCode'] != null) {
          userCountry = data['countryCode'];
          await prefs.setString('cached_user_country', userCountry);
        }
      }
      _initialized = true;
    } catch (e) {
      print('LocationHelper Error: $e');
    }
  }
}
