import re

with open('lib/widgets/next_episode_tracker.dart', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find("void _airingState(Map<String, dynamic> nep, Map<String, dynamic>? lep, Map<String, dynamic> tmdb) {")
end_idx = text.find("void _completedState(", start_idx)

new_method = """void _airingState(Map<String, dynamic> nep, Map<String, dynamic>? lep, Map<String, dynamic> tmdb) {
    final airStr = nep['air_date']?.toString() ?? '';
    final epNum = nep['episode_number'] ?? 1;
    final season = nep['season_number'] ?? 1;
    final total = tmdb['number_of_episodes'] ?? 0;
    final displayX = season > 1 ? '$epNum (Mùa $season)' : epNum.toString();
    try {
      final now = DateTime.now();
      final today = DateTime(now.year, now.month, now.day);
      final airDateStr = airStr.split('T').first;
      final airDate = DateTime.parse(airDateStr);
      final diff = airDate.difference(today).inDays;
      final fDate = _fmtDate(airDate);
      
      bool hasSource = false;
      if (widget.movie != null) {
        final epPattern = RegExp(r'\b' + epNum.toString() + r'\b');
        for (var server in widget.movie!.episodes) {
          if (server.items.any((ep) => epPattern.hasMatch(ep.name) || ep.name.toLowerCase() == 'full')) {
            hasSource = true;
            break;
          }
        }
      }

      final isFinale = total > 0 && epNum == total;
      final isToday = diff == 0;

      String key;
      if (isToday && hasSource && isFinale)        { key = 'ep_msg_today_finale_available'; _progressKey = 'party'; }
      else if (isToday && !hasSource && isFinale)  { key = 'ep_msg_today_finale_unavailable'; _progressKey = 'rage'; }
      else if (isToday && hasSource)               { key = 'ep_msg_today_available'; _progressKey = 'party'; }
      else if (isToday && !hasSource)              { key = 'ep_msg_today_unavailable'; _progressKey = 'rage'; }
      else if (diff < 0)                           { key = 'ep_msg_past_missed'; _progressKey = 'chill'; }
      else if (diff == 1)                          { key = 'ep_msg_tomorrow'; _progressKey = 'tense'; }
      else {
        final ratio = total > 0 ? epNum / total : 0.5;
        if (ratio < 0.45)      { key = 'ep_msg_future_first_half'; _progressKey = 'chill'; }
        else if (ratio < 0.82) { key = 'ep_msg_future_second_half'; _progressKey = 'tense'; }
        else                   { key = 'ep_msg_future_penultimate'; _progressKey = 'tense'; }
      }

      final phrases = L10n.tList(key);
      final idx = widget.phraseSeed % (phrases.isEmpty ? 1 : phrases.length);
      _msg = (phrases.isEmpty ? 'Tập $displayX: $airStr' : phrases[idx])
          .replaceAll('{X}', displayX).replaceAll('{DATE}', fDate).replaceAll('{DIFF}', diff.abs().toString());
    } catch (_) { _msg = 'Tập $epNum: $airStr'; }
  }

  """

new_text = text[:start_idx] + new_method + text[end_idx:]

with open('lib/widgets/next_episode_tracker.dart', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Patched _airingState successfully")
