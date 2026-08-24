import os

content = """import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:confetti/confetti.dart';
import 'package:lottie/lottie.dart';
import '../models/movie.dart';
import '../utils/l10n.dart';

enum ActionGroup { fireworks, shake, float, fall, shimmer }

class NextEpisodeTracker extends StatefulWidget {
  final Movie? movie;
  final Map<String, dynamic>? tmdbDetails;
  final int phraseSeed;

  const NextEpisodeTracker({
    Key? key,
    required this.movie,
    required this.tmdbDetails,
    required this.phraseSeed,
  }) : super(key: key);

  @override
  State<NextEpisodeTracker> createState() => _NextEpisodeTrackerState();
}

class _NextEpisodeTrackerState extends State<NextEpisodeTracker> with SingleTickerProviderStateMixin {
  late ConfettiController _confettiController;
  bool _isAnimatingText = false;
  
  String _msg = '';
  ActionGroup _currentGroup = ActionGroup.shimmer;
  String _stickerUrl = '';

  @override
  void initState() {
    super.initState();
    _confettiController = ConfettiController(duration: const Duration(seconds: 2));
    _calculateLogic();
  }

  @override
  void didUpdateWidget(covariant NextEpisodeTracker oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.movie?.id != oldWidget.movie?.id || widget.tmdbDetails != oldWidget.tmdbDetails) {
      _calculateLogic();
    }
  }

  @override
  void dispose() {
    _confettiController.dispose();
    super.dispose();
  }

  String getWeekday(int w) {
    if (L10n.currentLang == 'en') {
      const d = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
      return d[w - 1];
    } else {
      return w == 7 ? 'CN' : 'T${w + 1}';
    }
  }

  void _calculateLogic() {
    if (widget.movie == null) return;
    
    int currentEpNum = 0;
    try {
      if (widget.movie!.currentEpisode.isNotEmpty) {
        if (widget.movie!.currentEpisode.toLowerCase().contains("full")) {
          currentEpNum = 9999;
        } else {
          final m = RegExp(r'\\d+').firstMatch(widget.movie!.currentEpisode);
          if (m != null) currentEpNum = int.tryParse(m.group(0)!) ?? 0;
        }
      }
    } catch(e){}

    final nextEpMap = widget.tmdbDetails != null ? widget.tmdbDetails!['next_episode_to_air'] : null;
    if (nextEpMap != null && nextEpMap['air_date'] != null) {
      final airDateStr = nextEpMap['air_date'];
      int nextEpNum = nextEpMap['episode_number'] ?? 0;
      int totalEps = widget.tmdbDetails!['number_of_episodes'] ?? 0;
      if (totalEps <= 0) totalEps = int.tryParse(widget.movie!.totalEpisodes) ?? 0;
      
      bool isAvailable = currentEpNum >= nextEpNum;
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
          _currentGroup = ActionGroup.float;
          _stickerUrl = 'https://raw.githubusercontent.com/Tien360/mytv4u/main/assets/lottie/chill.json';
        } else if (diff == 0) {
          if (!isAvailable) {
            phrases = isFinale ? L10n.tList('ep_msg_today_pending_finale') : L10n.tList('ep_msg_today_pending');
            _currentGroup = ActionGroup.shake;
            _stickerUrl = 'https://raw.githubusercontent.com/Tien360/mytv4u/main/assets/lottie/angry.json';
          } else {
            phrases = isFinale ? L10n.tList('ep_msg_today_available_finale') : L10n.tList('ep_msg_today_available');
            _currentGroup = ActionGroup.fireworks;
            _stickerUrl = 'https://raw.githubusercontent.com/Tien360/mytv4u/main/assets/lottie/party.json';
          }
        } else if (diff < 0 && diff >= -3 && isFinale && isAvailable) {
          phrases = L10n.tList('ep_msg_just_finished_finale');
          _currentGroup = ActionGroup.fall;
          _stickerUrl = 'https://raw.githubusercontent.com/Tien360/mytv4u/main/assets/lottie/cry.json';
        } else {
          if (totalEps > 0 && currentEpNum >= totalEps) {
            if (widget.movie!.type.toLowerCase() == 'single' || widget.movie!.type.toLowerCase() == 'movie' || totalEps <= 10) {
                phrases = L10n.tList('ep_msg_completed_short');
            } else {
                phrases = L10n.tList('ep_msg_completed_long');
            }
          } else {
            phrases = L10n.tList('ep_msg_past_missed');
          }
          _currentGroup = ActionGroup.shimmer;
          _stickerUrl = 'https://raw.githubusercontent.com/Tien360/mytv4u/main/assets/lottie/sleep.json';
        }
        
        if (phrases.isEmpty) phrases = [L10n.t('next_episode') ?? 'Tập tiếp theo: $airDateStr'];
        final random = widget.phraseSeed % phrases.length;
        _msg = phrases[random];
        
        String fDate = L10n.currentLang == 'vi' ? '(${getWeekday(airDate.weekday)} ${airDate.day}/${airDate.month}/${airDate.year})' : '(${getWeekday(airDate.weekday)} $airDateStr)';
        String nextInfo = '';
        if (diff == 0 && isAvailable && !isFinale) {
           final estDate = airDate.add(const Duration(days: 7));
           final estStr = L10n.currentLang == 'vi' ? '(${getWeekday(estDate.weekday)} ${estDate.day}/${estDate.month}/${estDate.year})' : '(${getWeekday(estDate.weekday)} ${estDate.year}-${estDate.month.toString().padLeft(2, '0')}-${estDate.day.toString().padLeft(2, '0')})';
           List<String> nextArr = [
             L10n.t('ep_msg_next_estimated', {'DATE': estStr, 'X': (nextEpNum + 1).toString()}),
             L10n.t('ep_msg_next_unknown')
           ];
           nextInfo = nextArr[DateTime.now().millisecondsSinceEpoch % nextArr.length];
        }

        _msg = _msg.replaceAll('{X}', nextEpNum.toString());
        _msg = _msg.replaceAll('{DATE}', fDate);
        _msg = _msg.replaceAll('{DIFF}', diff.abs().toString());
        _msg = _msg.replaceAll('{NEXT_INFO}', nextInfo);

      } catch (e) {
        _msg = 'Tập $nextEpNum: $airDateStr';
        _currentGroup = ActionGroup.shimmer;
      }
    } else {
       int totalEps = widget.tmdbDetails != null ? widget.tmdbDetails!['number_of_episodes'] ?? 0 : 0;
       if (totalEps <= 0) totalEps = int.tryParse(widget.movie!.totalEpisodes) ?? 0;
       
       List<String> phrases = [];
       if (widget.movie!.type.toLowerCase() == 'single' || widget.movie!.type.toLowerCase() == 'movie' || totalEps <= 10) {
          phrases = L10n.tList('ep_msg_completed_short');
       } else {
          phrases = L10n.tList('ep_msg_completed_long');
       }
       final random = widget.phraseSeed % phrases.length;
       _msg = phrases[random];
       _currentGroup = ActionGroup.shimmer;
       _stickerUrl = 'https://raw.githubusercontent.com/Tien360/mytv4u/main/assets/lottie/sleep.json';
    }
    
    setState(() {});
  }

  void _triggerEffect() async {
    if (_isAnimatingText) return;
    setState(() => _isAnimatingText = true);
    
    _showLottieSticker();
    
    switch (_currentGroup) {
      case ActionGroup.fireworks:
        _confettiController.play();
        break;
      case ActionGroup.shake:
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(L10n.currentLang == 'vi' ? 'Đang hối thúc Admin Mux! Bạn đợi xíu nhé ⏳' : 'Pinging the admin! Please wait ⏳'), duration: const Duration(seconds: 2)),
        );
        break;
      case ActionGroup.float:
        _showFloatingParticles(['🍿', '🎬', '🥤'], isFalling: false);
        break;
      case ActionGroup.fall:
        _showFloatingParticles(['❤️', '🌟', '✨'], isFalling: true);
        break;
      case ActionGroup.shimmer:
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(L10n.currentLang == 'vi' ? 'Tắt điện thoại và đi ngủ đi nhé! Cày phim muộn rồi 🛏️' : 'Time to sleep! Don\'t binge watch all night 🛏️'), duration: const Duration(seconds: 2)),
        );
        break;
    }
    
    await Future.delayed(const Duration(seconds: 2));
    if (mounted) setState(() => _isAnimatingText = false);
  }

  void _showLottieSticker() {
    showDialog(
      context: context,
      barrierColor: Colors.transparent,
      builder: (context) {
        Future.delayed(const Duration(milliseconds: 2500), () {
          if (Navigator.of(context).canPop()) {
            Navigator.of(context).pop();
          }
        });
        return Center(
          child: IgnorePointer(
            child: SizedBox(
              width: 250,
              height: 250,
              child: Lottie.network(
                _stickerUrl, 
                errorBuilder: (context, error, stackTrace) => const SizedBox(),
              ),
            ),
          ),
        );
      },
    );
  }

  void _showFloatingParticles(List<String> particles, {required bool isFalling}) {
    final overlay = Overlay.of(context);
    final renderBox = context.findRenderObject() as RenderBox?;
    if (renderBox == null) return;
    
    final size = MediaQuery.of(context).size;
    final startY = isFalling ? 0.0 : size.height;
    final endY = isFalling ? size.height : 0.0;
    
    final random = Random();
    
    for (int i = 0; i < 15; i++) {
      final startX = random.nextDouble() * size.width;
      final endX = startX + (random.nextDouble() - 0.5) * 100;
      final delay = random.nextInt(500);
      final duration = 1500 + random.nextInt(1000);
      final p = particles[random.nextInt(particles.length)];
      
      late OverlayEntry entry;
      entry = OverlayEntry(
        builder: (context) {
          return TweenAnimationBuilder(
            tween: Tween<double>(begin: 0, end: 1),
            duration: Duration(milliseconds: duration),
            builder: (context, double value, child) {
              if (value == 1) {
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  if (entry.mounted) entry.remove();
                });
              }
              final currentY = startY + (endY - startY) * value;
              final currentX = startX + (endX - startX) * value;
              final opacity = value < 0.2 ? value * 5 : (value > 0.8 ? (1 - value) * 5 : 1.0);
              
              return Positioned(
                left: currentX,
                top: currentY,
                child: Opacity(
                  opacity: opacity,
                  child: Text(p, style: const TextStyle(fontSize: 32, decoration: TextDecoration.none)),
                ),
              );
            },
          );
        }
      );
      
      Future.delayed(Duration(milliseconds: delay), () {
        overlay.insert(entry);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_msg.isEmpty) return const SizedBox.shrink();

    Widget textWidget = Text(
      _msg,
      style: TextStyle(
        fontSize: 15,
        fontWeight: FontWeight.w500,
        color: _isAnimatingText && _currentGroup == ActionGroup.shake ? Colors.redAccent : Colors.white,
        fontStyle: FontStyle.italic,
      ),
    );

    // Apply text animations
    if (_isAnimatingText) {
      if (_currentGroup == ActionGroup.fireworks) {
        textWidget = textWidget.animate().bounce();
      } else if (_currentGroup == ActionGroup.shake) {
        textWidget = textWidget.animate().shake(hz: 10, offset: const Offset(5, 0));
      } else if (_currentGroup == ActionGroup.shimmer) {
        textWidget = textWidget.animate().shimmer(duration: 1.seconds, color: Colors.blueAccent);
      } else {
        textWidget = textWidget.animate().fade().scale();
      }
    }

    return Padding(
      padding: const EdgeInsets.only(top: 16.0),
      child: GestureDetector(
        onTap: _triggerEffect,
        child: MouseRegion(
          cursor: SystemMouseCursors.click,
          child: Stack(
            clipBehavior: Clip.none,
            alignment: Alignment.center,
            children: [
              textWidget,
              if (_currentGroup == ActionGroup.fireworks)
                Positioned(
                  top: -20,
                  child: ConfettiWidget(
                    confettiController: _confettiController,
                    blastDirectionality: BlastDirectionality.explosive,
                    particleDrag: 0.05,
                    emissionFrequency: 0.05,
                    numberOfParticles: 30,
                    gravity: 0.1,
                    colors: const [Colors.green, Colors.blue, Colors.pink, Colors.orange, Colors.purple],
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
"""
os.makedirs("lib/widgets", exist_ok=True)
with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Created next_episode_tracker.dart")
