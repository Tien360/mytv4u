import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:html/parser.dart' as html_parser;

import '../models/sport_match.dart';

class SportApi {
  static Future<List<SportMatch>> getMatches() async {
    try {
      final res = await http.get(Uri.parse('https://tinhlagi.pro/sport/'));
      if (res.statusCode == 200) {
        final doc = html_parser.parse(res.body);
        final buttons = doc.querySelectorAll('.match-btn');
        List<SportMatch> matches = [];

        for (var btn in buttons) {
          final title = btn.attributes['data-title'] ?? '';
          final time = btn.attributes['data-time'] ?? '';
          final league = btn.attributes['data-league'] ?? 'Giải đấu khác';
          final sourcesStr = btn.attributes['data-sources'] ?? '[]';
          
          List<SportSource> sources = [];
          try {
            final decoded = json.decode(sourcesStr.replaceAll('&quot;', '"')) as List;
            sources = decoded.map((s) => SportSource.fromJson(s as Map<String, dynamic>)).toList();
          } catch (e) {
            print('Error parsing sport sources: $e');
          }

          final statusBadge = btn.querySelector('.status-badge');
          String status = 'Sắp diễn ra';
          if (statusBadge != null && statusBadge.text.toLowerCase().contains('live')) {
            status = 'Live';
          }
          
          // Tạo id duy nhất dựa trên tên và thời gian
          final id = base64UrlEncode(utf8.encode(title + time));

          matches.add(SportMatch(
            id: id,
            title: title,
            time: time,
            league: league,
            status: status,
            sources: sources,
          ));
        }
        return matches;
      }
    } catch (e) {
      print('Error getting sport matches: $e');
    }
    return [];
  }
}
