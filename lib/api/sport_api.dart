import 'dart:convert';
import 'package:http/http.dart' as http;
import '../utils/l10n.dart';
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
          final league = btn.attributes['data-league'] ?? L10n.t('other-leagues') ?? 'Giải đấu khác';
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
          if (statusBadge != null && statusBadge.classes.contains('status-live')) {
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

  static Future<LivescoreData?> getLiveScores() async {
    try {
      final res = await http.get(Uri.parse('https://tinhlagi.pro/sport/livescore_data.json?t=${DateTime.now().millisecondsSinceEpoch}'));
      if (res.statusCode == 200) {
        final decoded = json.decode(res.body);
        return LivescoreData.fromJson(decoded);
      }
    } catch (e) {
      print('Error getting live scores: $e');
    }
    return null;
  }
}

