import json

with open('lib/widgets/next_episode_tracker.dart', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find("void _airingState(")
end_idx = text.find("void _completedState(", start_idx)

new_method = r"""  void _airingState(Map<String, dynamic> nep, Map<String, dynamic>? lep, Map<String, dynamic> tmdb) {
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
      bool isMissingPrevious = false;
      String missingEp = '';
      
      if (widget.movie != null) {
        final epPattern = RegExp('\\b' + epNum.toString() + '\\b');
        for (var server in widget.movie!.episodes) {
          if (server.items.any((ep) => epPattern.hasMatch(ep.name) || ep.name.toLowerCase() == 'full')) {
            hasSource = true;
            break;
          }
        }
        
        if (lep != null) {
          final lepNum = lep['episode_number'] ?? 0;
          if (lepNum > 0 && !hasSource) {
            bool hasLep = false;
            final lepPattern = RegExp('\\b' + lepNum.toString() + '\\b');
            for (var server in widget.movie!.episodes) {
              if (server.items.any((ep) => lepPattern.hasMatch(ep.name) || ep.name.toLowerCase() == 'full')) {
                hasLep = true;
                break;
              }
            }
            if (!hasLep) {
              isMissingPrevious = true;
              missingEp = (season > 1 ? '$lepNum (Mùa $season)' : lepNum.toString());
            }
          }
        }
      }

      final isFinale = total > 0 && epNum == total;
      final isToday = diff == 0;

      String key;
      if (isMissingPrevious)                       { key = 'ep_msg_previous_missing'; _progressKey = 'rage'; }
      else if (isToday && hasSource && isFinale)   { key = 'ep_msg_today_finale_available'; _progressKey = 'party'; }
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
          .replaceAll('{X}', displayX)
          .replaceAll('{DATE}', fDate)
          .replaceAll('{DIFF}', diff.abs().toString())
          .replaceAll('{LAST_EP}', missingEp);
    } catch (_) { _msg = 'Tập $epNum: $airStr'; }
  }

"""

new_text = text[:start_idx] + new_method + text[end_idx:]

with open('lib/widgets/next_episode_tracker.dart', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Patched _airingState successfully")
