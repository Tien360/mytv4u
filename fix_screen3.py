import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

replacement = """                                              Builder(
                                                builder: (context) {
                                                  String msg = '';
                                                  
                                                  int currentEpNum = 0;
                                                  try {
                                                    if (_movie!.currentEpisode.isNotEmpty) {
                                                      if (_movie!.currentEpisode.toLowerCase().contains("full")) {
                                                        currentEpNum = 9999;
                                                      } else {
                                                        final m = RegExp(r'\\d+').firstMatch(_movie!.currentEpisode);
                                                        if (m != null) currentEpNum = int.tryParse(m.group(0)!) ?? 0;
                                                      }
                                                    }
                                                  } catch(e){}
                                              
                                                  final nextEpMap = _tmdbDetails!['next_episode_to_air'];
                                                  if (nextEpMap != null && nextEpMap['air_date'] != null) {
                                                    final airDateStr = nextEpMap['air_date'];
                                                    int nextEpNum = nextEpMap['episode_number'] ?? 0;
                                                    int totalEps = _tmdbDetails!['number_of_episodes'] ?? 0;
                                                    if (totalEps <= 0) totalEps = int.tryParse(_movie!.totalEpisodes) ?? 0;
                                                    
                                                    bool isAvailable = currentEpNum >= nextEpNum;
                                                    bool isFirstHalf = totalEps > 0 && nextEpNum < (totalEps / 2).ceil();
                                                    bool isHalfway = nextEpNum > 0 && totalEps > 0 && nextEpNum == (totalEps / 2).ceil();
                                                    bool isSecondHalf = totalEps > 0 && nextEpNum > (totalEps / 2).ceil() && nextEpNum < totalEps - 1;
                                                    bool isPenultimate = totalEps > 0 && nextEpNum == totalEps - 1;
                                                    bool isFinale = totalEps > 0 && nextEpNum == totalEps;
                                              
                                                    try {
                                                      final airDate = DateTime.parse(airDateStr);
                                                      final now = DateTime.now();
                                                      final today = DateTime(now.year, now.month, now.day);
                                                      final aDate = DateTime(airDate.year, airDate.month, airDate.day);
                                                      final diff = aDate.difference(today).inDays;
                                                      
                                                      List<String> phrases = [];
                                                      
                                                      if (diff > 0) {
                                                        if (isFinale) {
                                                          phrases = L10n.tList('ep_msg_future_finale');
                                                        } else if (isPenultimate) {
                                                          phrases = L10n.tList('ep_msg_future_penultimate');
                                                        } else if (isSecondHalf) {
                                                          phrases = L10n.tList('ep_msg_future_second_half');
                                                        } else if (isHalfway) {
                                                          phrases = L10n.tList('ep_msg_future_halfway');
                                                        } else {
                                                          phrases = L10n.tList('ep_msg_future_first_half');
                                                        }
                                                      } else if (diff == 0) {
                                                        if (!isAvailable) {
                                                          phrases = isFinale ? L10n.tList('ep_msg_today_pending_finale') : L10n.tList('ep_msg_today_pending');
                                                        } else {
                                                          phrases = isFinale ? L10n.tList('ep_msg_today_available_finale') : L10n.tList('ep_msg_today_available');
                                                        }
                                                      } else if (diff < 0 && diff >= -3 && isFinale && isAvailable) {
                                                        // 3-day grace period for finale
                                                        phrases = L10n.tList('ep_msg_just_finished_finale');
                                                      } else {
                                                        // Aired in the past but not finale grace period, or missing TMDB updates
                                                        if (totalEps > 0 && currentEpNum >= totalEps) {
                                                          // Completed old series
                                                          if (_movie!.type.toLowerCase() == 'single' || _movie!.type.toLowerCase() == 'movie' || totalEps <= 10) {
                                                              phrases = L10n.tList('ep_msg_completed_short');
                                                          } else {
                                                              phrases = L10n.tList('ep_msg_completed_long');
                                                          }
                                                        } else {
                                                          phrases = L10n.tList('ep_msg_past_missed');
                                                        }
                                                      }
                                                      
                                                      if (phrases.isEmpty) phrases = [L10n.t('next_episode') ?? 'Tập tiếp theo: $airDateStr'];
                                                      
                                                      final random = DateTime.now().millisecondsSinceEpoch % phrases.length;
                                                      msg = phrases[random];
                                                      
                                                      String fDate = L10n.currentLang == 'vi' ? '${airDate.day}/${airDate.month}/${airDate.year}' : airDateStr;
                                                      
                                                      String nextInfo = '';
                                                      if (diff == 0 && isAvailable && !isFinale) {
                                                         final estDate = airDate.add(const Duration(days: 7));
                                                         final estStr = L10n.currentLang == 'vi' ? '${estDate.day}/${estDate.month}/${estDate.year}' : '${estDate.year}-${estDate.month.toString().padLeft(2, '0')}-${estDate.day.toString().padLeft(2, '0')}';
                                                         List<String> nextArr = [
                                                           L10n.t('ep_msg_next_estimated', {'DATE': estStr, 'X': (nextEpNum + 1).toString()}),
                                                           L10n.t('ep_msg_next_unknown')
                                                         ];
                                                         nextInfo = nextArr[DateTime.now().millisecondsSinceEpoch % nextArr.length];
                                                      }
                                              
                                                      msg = msg.replaceAll('{X}', nextEpNum.toString());
                                                      msg = msg.replaceAll('{DATE}', fDate);
                                                      msg = msg.replaceAll('{DIFF}', diff.abs().toString());
                                                      msg = msg.replaceAll('{NEXT_INFO}', nextInfo);
                                              
                                                    } catch (e) {
                                                      msg = 'Tập $nextEpNum: $airDateStr';
                                                    }
                                                  } else {
                                                     int totalEps = _tmdbDetails!['number_of_episodes'] ?? 0;
                                                     if (totalEps <= 0) totalEps = int.tryParse(_movie!.totalEpisodes) ?? 0;
                                                     
                                                     List<String> phrases = [];
                                                     if (_movie!.type.toLowerCase() == 'single' || _movie!.type.toLowerCase() == 'movie' || totalEps <= 10) {
                                                        phrases = L10n.tList('ep_msg_completed_short');
                                                     } else {
                                                        phrases = L10n.tList('ep_msg_completed_long');
                                                     }
                                                     final random = DateTime.now().millisecondsSinceEpoch % phrases.length;
                                                     msg = phrases[random];
                                                  }
                                              
                                                  if (msg.isNotEmpty) {
                                                    return Padding(
                                                      padding: const EdgeInsets.only(top: 16.0),
                                                      child: Text(
                                                        msg,
                                                        style: const TextStyle(
                                                          fontSize: 15,
                                                          fontWeight: FontWeight.w500,
                                                          color: Colors.white,
                                                          fontStyle: FontStyle.italic,
                                                        ),
                                                      ),
                                                    );
                                                  }
                                                  return const SizedBox.shrink();
                                                }
                                              ),
"""

text = re.sub(r'Builder\(\s*builder: \(context\) \{\s*String msg = \'\'\;.*?return const SizedBox\.shrink\(\)\;\s*\}\s*\)\,', lambda m: replacement, text, flags=re.DOTALL)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated movie_detail_screen.dart")
