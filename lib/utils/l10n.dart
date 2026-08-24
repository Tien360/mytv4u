import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

class L10n {
  static const List<String> supportedLangs = ['vi', 'en'];
  static String currentLang = 'vi';
  static Map<String, dynamic> _localizedStrings = {};

  static Future<void> load([String? langCode]) async {
    final prefs = await SharedPreferences.getInstance();
    if (langCode != null && supportedLangs.contains(langCode)) {
      currentLang = langCode;
      await prefs.setString('app_lang', langCode);
    } else {
      currentLang = prefs.getString('app_lang') ?? 'vi';
      if (!supportedLangs.contains(currentLang)) {
        currentLang = 'vi';
      }
    }

    try {
      String jsonString = await rootBundle.loadString('assets/langs/$currentLang.json');
      _localizedStrings = json.decode(jsonString);
    } catch (e) {
      print('Error loading language file: $e');
      _localizedStrings = {};
    }
  }

  static String t(String key, [Map<String, String>? params]) {
    String text = _localizedStrings[key] ?? key;
    if (text == key && currentLang == 'vi') {
      if (key == 'trailer_stop') text = 'Dừng Trailer';
      if (key == 'trailer_search') text = 'Tìm Trailer';
      if (key == 'trailer_replay') text = 'Phát lại Trailer';
      if (key == 'trailer_play') text = 'Phát Trailer';
    }

    if (params != null) {
      params.forEach((k, v) {
        text = text.replaceAll('{$k}', v);
      });
    }
    return text;
  }

  static List<String> tList(String key) {
    var val = _localizedStrings[key];
    if (val is List) {
      return val.map((e) => e.toString()).toList();
    }
    return [t(key)];
  }
}