import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:confetti/confetti.dart';
import 'package:lottie/lottie.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/movie.dart';
import '../utils/l10n.dart';

enum ScenarioGroup { universal, genre, progress, legendary, spam }
enum OutputType { sticker, particles, toast }
enum SupportedGenre {
  action, romance, comedy, historical, psychological, crime, scifi, horror, animation, lgbt
}

  const Map<SupportedGenre, List<String>> _genreStickers = {
    SupportedGenre.action: ['assets/lottie/lf20_fyye8szy.json', 'assets/easter/dynamite.png', 'assets/lottie/noto_1f4a5.json', 'assets/lottie/noto_1f4a3.json', 'assets/lottie/noto_1f525.json'],
    SupportedGenre.romance: ['assets/lottie/lf20_qp1q7mct.json', 'assets/lottie/lf20_ydo1amjm.json', 'assets/easter/fluent_heart.png', 'assets/easter/teddy.png', 'assets/lottie/noto_1f496.json', 'assets/lottie/noto_1f970.json', 'assets/lottie/noto_1f498.json', 'assets/lottie/noto_1f48d.json', 'assets/lottie/noto_1f339.json'],
    SupportedGenre.comedy: ['assets/easter/fluent_clown.png', 'assets/easter/tissue.png', 'assets/lottie/noto_1f602.json', 'assets/lottie/noto_1f923.json', 'assets/lottie/noto_1f92a.json', 'assets/lottie/noto_1f921.json', 'assets/lottie/noto_1f606.json'],
    SupportedGenre.historical:    ['assets/lottie/lf20_ofa3xwo7.json', 'assets/lottie/lf20_3rqwsqnj.json', '⛩️', '🗡️', '🏯', '📜', '🎎'],
    SupportedGenre.psychological: ['assets/lottie/lf20_aZTdD5.json', 'assets/lottie/noto_1f9e0.json', 'assets/lottie/noto_1f635_200d_1f4ab.json', 'assets/lottie/noto_1f3ad.json', 'assets/lottie/noto_1f300.json', 'assets/lottie/noto_1f441.json'],
    SupportedGenre.crime: ['assets/lottie/lf20_5tl1xxnz.json', 'assets/lottie/lf20_kkflmtur.json', 'assets/lottie/noto_1fa78.json'],
    SupportedGenre.scifi: ['assets/lottie/lf20_khzniaya.json', 'assets/lottie/lf20_syqnfe7c.json', 'assets/easter/fluent_alien.png', 'assets/easter/ufo.png', 'assets/lottie/noto_1f680.json', 'assets/lottie/noto_1f47d.json', 'assets/lottie/noto_1f916.json', 'assets/lottie/noto_1f6f8.json', 'assets/lottie/noto_1f30c.json'],
    SupportedGenre.horror: ['assets/lottie/lf20_m9zragkd.json', 'assets/easter/fluent_ghost.png', 'assets/easter/fluent_skull.png', 'assets/lottie/noto_1f47b.json', 'assets/lottie/noto_1f480.json', 'assets/lottie/noto_1f383.json'],
    SupportedGenre.animation: ['assets/lottie/lf20_touohxv0.json', 'assets/lottie/lf20_xlmz9xwm.json', 'assets/lottie/noto_1f984.json', 'assets/lottie/noto_1f308.json', 'assets/lottie/noto_1f388.json', 'assets/lottie/noto_1fa84.json'],
    SupportedGenre.lgbt: ['assets/lottie/noto_1f3f3.json'],
  };

  const Map<String, List<String>> _progressStickers = {
    'party': ['assets/easter/fluent_party.png', 'assets/lottie/noto_1f389.json', 'assets/lottie/noto_1f38a.json', 'assets/lottie/noto_1f942.json', 'assets/lottie/noto_1f973.json', 'assets/lottie/noto_1f381.json'],
    'cry': ['assets/lottie/lf20_qp1q7mct.json', 'assets/easter/fluent_clown.png', 'assets/easter/tissue.png', 'assets/easter/fluent_crying.png', 'assets/lottie/noto_1f62d.json', 'assets/lottie/noto_1f494.json', 'assets/lottie/noto_1f940.json', 'assets/lottie/noto_1f622.json'],
    'rage': ['assets/lottie/lf20_5tl1xxnz.json', 'assets/lottie/lf20_syqnfe7c.json', 'assets/easter/dynamite.png', 'assets/easter/fluent_angry.png', 'assets/lottie/noto_1f92c.json', 'assets/lottie/noto_1f30b.json', 'assets/lottie/noto_1f620.json'],
    'chill': ['assets/lottie/noto_1f37f.json', 'assets/lottie/noto_2615.json'],
    'tense': ['assets/lottie/lf20_m9zragkd.json', 'assets/lottie/noto_1f631.json', 'assets/lottie/noto_1f630.json', 'assets/lottie/noto_1f976.json', 'assets/lottie/noto_1f440.json', 'assets/lottie/noto_23f3.json'],
  };

const Map<SupportedGenre, List<String>> _genreParticles = {
  SupportedGenre.action:        ['\u{1F4A5}', '\u{1F525}', '\u26A1', '\u{1F4A3}', '\u{1F3C6}'],
  SupportedGenre.romance:       ['\u2764\uFE0F', '\u{1F339}', '\u{1F495}', '\u{1F98B}', '\u{1F48C}'],
  SupportedGenre.comedy:        ['\u{1F602}', '\u{1F3AD}', '\u{1F389}', '\u{1F923}', '\u{1F44F}'],
  SupportedGenre.historical:    ['\u{1F4DC}', '\u{1F451}', '\u2694\uFE0F', '\u{1F3EF}', '\u{1FAB9}'],
  SupportedGenre.psychological: ['\u{1F9E0}', '\u{1F300}', '\u2753', '\u{1F3AD}', '\u{1F635}'],
  SupportedGenre.crime:         ['\u{1F50D}', '\u{1F694}', '\u{1F512}', '\u{1F575}', '\u2696\uFE0F'],
  SupportedGenre.scifi:         ['\u{1F6F8}', '\u{1F680}', '\u2B50', '\u{1F916}', '\u{1F30C}'],
  SupportedGenre.horror:        ['\u{1F47B}', '\u{1F577}\uFE0F', '\u{1FA78}', '\u2620\uFE0F', '\u{1F987}'],
  SupportedGenre.animation:     ['\u{1F308}', '\u{1F984}', '\u2728', '\u{1F31F}', '\u{1F3A0}'],
  SupportedGenre.lgbt:          ['\u{1F3F3}\uFE0F\u200D\u{1F308}', '\u2764\uFE0F', '\u{1F49C}', '\u{1F49B}', '\u{1F308}'],
};

const Map<SupportedGenre, List<String>> _genreKeywords = {
  SupportedGenre.action:        ['hanh dong', 'action', 'h\u00e0nh \u0111\u1ed9ng'],
  SupportedGenre.romance:       ['tinh cam', 'romance', 't\u00ecnh c\u1ea3m', 'romantic'],
  SupportedGenre.comedy:        ['hai huoc', 'comedy', 'h\u00e0i h\u01b0\u1edbc', 'h\u00e0i'],
  SupportedGenre.historical:    ['co trang', 'historical', 'c\u1ed5 trang', 'period'],
  SupportedGenre.psychological: ['tam ly', 'psychological', 't\u00e2m l\u00fd', 'thriller', 'mystery'],
  SupportedGenre.crime:         ['hinh su', 'crime', 'h\u00ecnh s\u1ef1', 'detective', 'criminal'],
  SupportedGenre.scifi:         ['vien tuong', 'sci-fi', 'vi\u1ec5n t\u01b0\u1edfng', 'fantasy', 'science fiction'],
  SupportedGenre.horror:        ['kinh di', 'horror', 'kinh d\u1ecb', 'scary'],
  SupportedGenre.animation:     ['hoat hinh', 'animation', 'ho\u1ea1t h\u00ecnh', 'anime', 'animated'],
  SupportedGenre.lgbt:          ['lgbt', 'dam my', '\u0111am m\u1ef9', 'bach hop', 'b\u00e1ch h\u1ee3p', 'bl', 'gl', 'yaoi', 'yuri', 'boy love', 'girl love', 'lgbtq'],
};

const List<String> _universalStickers = [
  'https://assets1.lottiefiles.com/packages/lf20_yrtouvgn.json',
  'https://assets4.lottiefiles.com/packages/lf20_oqyiaqx4.json',
  'https://assets3.lottiefiles.com/packages/lf20_jbb4x5qp.json',
  'https://assets6.lottiefiles.com/packages/lf20_uw0knnbz.json',
];
const List<String> _universalParticles = ['\u{1F37F}', '\u{1F3AC}', '\u{1F964}', '\u{1F3A5}', '\u2B50'];

const List<String> _sleepStickers = [
  'https://assets3.lottiefiles.com/packages/lf20_ks5srqfr.json',
  'https://assets4.lottiefiles.com/packages/lf20_fcfjwiyq.json',
  'https://assets7.lottiefiles.com/packages/lf20_f0iuc6cj.json',
];
const List<String> _sleepParticles = ['\u{1F4A4}', '\u{1F634}', '\u{1F319}', '\u2B50', '\u{1F6CF}\uFE0F'];

const String _legendarySticker = 'assets/lottie/lf20_ofa3xwo7.json';

class NextEpisodeTracker extends StatefulWidget {
  final Movie? movie;
  final Map<String, dynamic>? tmdbDetails;
  final int phraseSeed;
  const NextEpisodeTracker({Key? key, required this.movie, required this.tmdbDetails, required this.phraseSeed}) : super(key: key);
  @override
  State<NextEpisodeTracker> createState() => _NextEpisodeTrackerState();

  static Widget _buildLegendaryWidget() {
    return Center(
      child: Material(
        color: Colors.transparent,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('🙇‍♂️', style: TextStyle(fontSize: 140, decoration: TextDecoration.none))
                .animate(onPlay: (c) => c.repeat(reverse: true))
                .rotate(begin: -0.05, end: 0.1, duration: 600.ms)
                .moveY(begin: 0, end: 20, duration: 600.ms),
            const SizedBox(height: 24),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.85),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.amber, width: 2),
                boxShadow: [BoxShadow(color: Colors.amber.withOpacity(0.5), blurRadius: 20, spreadRadius: 2)],
              ),
              child: Text(
                L10n.currentLang == 'vi' 
                    ? 'Cảm ơn bạn đã đồng hành\ncùng MyTV4U ❤️' 
                    : 'Thank you for being\nwith MyTV4U ❤️',
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.amber, 
                  fontSize: 22, 
                  fontWeight: FontWeight.bold,
                  height: 1.4,
                ),
              ),
            ).animate().fade(duration: 800.ms).scale(curve: Curves.easeOutBack),
          ],
        ),
      ),
    );
  }

  static void triggerLegendaryFromOutside(BuildContext context) {
    final overlay = Overlay.of(context);
    late OverlayEntry entry;
    entry = OverlayEntry(builder: (ctx) {
      Future.delayed(const Duration(milliseconds: 3500), () { if (entry.mounted) entry.remove(); });
      return Positioned.fill(
        child: IgnorePointer(
          child: Container(
            color: Colors.black54,
            child: _buildLegendaryWidget(),
          ),
        ),
      );
    });
    overlay.insert(entry);
  }
}

class _NextEpisodeTrackerState extends State<NextEpisodeTracker> with SingleTickerProviderStateMixin {
  late ConfettiController _confettiController;
  bool _isAnimatingText = false;
  bool _easterEggsEnabled = true;
  String _msg = '';
  String _progressKey = 'chill';
  int _spamCount = 0;
  Timer? _spamTimer;
  List<SupportedGenre> _matchedGenres = [];

  @override
  void initState() {
    super.initState();
    _confettiController = ConfettiController(duration: const Duration(seconds: 3));
    _loadPref();
    _calculateLogic();
  }

  Future<void> _loadPref() async {
    final p = await SharedPreferences.getInstance();
    if (mounted) setState(() { _easterEggsEnabled = p.getBool('enable_easter_eggs') ?? true; });
  }

  @override
  void didUpdateWidget(covariant NextEpisodeTracker old) {
    super.didUpdateWidget(old);
    if (widget.movie?.slug != old.movie?.slug || widget.tmdbDetails != old.tmdbDetails) _calculateLogic();
  }

  @override
  void dispose() { _confettiController.dispose(); super.dispose(); }

  String _weekday(int w) {
    if (L10n.currentLang == 'en') return ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][w-1];
    return ['T2','T3','T4','T5','T6','T7','CN'][w-1];
  }

  String _fmtDate(DateTime d) {
    if (L10n.currentLang == 'en') return '(${_weekday(d.weekday)} ${d.year}-${d.month.toString().padLeft(2,'0')}-${d.day.toString().padLeft(2,'0')})';
    return '(${_weekday(d.weekday)} ${d.day}/${d.month}/${d.year})';
  }

  List<SupportedGenre> _matchGenres() {
    final raw = widget.movie?.genres ?? [];
    final found = <SupportedGenre>[];
    for (final g in SupportedGenre.values) {
      final kws = _genreKeywords[g]!;
      for (final r in raw) {
        if (kws.any((k) => r.toLowerCase().contains(k))) { if (!found.contains(g)) found.add(g); break; }
      }
    }
    return found;
  }

  void _calculateLogic() {
    _matchedGenres = _matchGenres();
    final tmdb = widget.tmdbDetails;
    if (tmdb == null || widget.movie == null) { setState(() => _msg = ''); return; }
    final nextEp = tmdb['next_episode_to_air'] as Map<String, dynamic>?;
    final lastEp = tmdb['last_episode_to_air'] as Map<String, dynamic>?;
    if (nextEp != null) _airingState(nextEp, lastEp, tmdb);
    else _completedState(tmdb);
    setState(() {});
  }

        void _airingState(Map<String, dynamic> nep, Map<String, dynamic>? lep, Map<String, dynamic> tmdb) {
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
      bool isVipAhead = false;
      int maxEpInApp = 0;
      String missingEp = '';
      
      if (widget.movie != null) {
        // Filter out auto-generated metadata sources that don't guarantee stream existence
        final reliableServers = widget.movie!.episodes.where((s) {
          final n = s.serverName.toLowerCase();
          return !n.contains('vidsrc') && !n.contains('vidapi') && !n.contains('p2p');
        }).toList();

        // Determine the maximum episode number in our reliable sources
        for (var server in reliableServers) {
          for (var ep in server.items) {
            final match = RegExp(r'\d+').firstMatch(ep.name);
            if (match != null) {
              final num = int.tryParse(match.group(0)!);
              if (num != null && num > maxEpInApp) maxEpInApp = num;
            }
          }
        }
        
        if (maxEpInApp > epNum) {
          isVipAhead = true;
        }

        final epPattern = RegExp('\\b' + epNum.toString() + '\\b');
        for (var server in reliableServers) {
          if (server.items.any((ep) => epPattern.hasMatch(ep.name) || ep.name.toLowerCase() == 'full')) {
            hasSource = true;
            break;
          }
        }
        
        if (lep != null) {
          final lepNum = lep['episode_number'] ?? 0;
          if (lepNum > 0 && !hasSource && !isVipAhead) {
            bool hasLep = false;
            final lepPattern = RegExp('\\b' + lepNum.toString() + '\\b');
            for (var server in reliableServers) {
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
      if (isVipAhead)                              { key = 'ep_msg_vip_ahead'; _progressKey = 'party'; }
      else if (isMissingPrevious)                  { key = 'ep_msg_previous_missing'; _progressKey = 'rage'; }
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
          .replaceAll('{LAST_EP}', missingEp)
          .replaceAll('{MAX_EP}', maxEpInApp.toString())
          .replaceAll('{NEXT_INFO}', '');
    } catch (_) { _msg = 'Tập $epNum: $airStr'; }
  }

void _completedState(Map<String, dynamic> tmdb) {
    final total = tmdb['number_of_episodes'] ?? int.tryParse(widget.movie!.totalEpisodes) ?? 0;
    final isShort = ['single','movie'].contains(widget.movie!.type.toLowerCase()) || total <= 10;
    final lep = tmdb['last_episode_to_air'] as Map<String, dynamic>?;
    if (lep != null) {
      try {
        final d = DateTime.parse(lep['air_date']?.toString() ?? '');
        if (DateTime.now().difference(d).inDays <= 3) {
          final p = L10n.tList('ep_msg_just_finished_finale');
          _msg = p[widget.phraseSeed % p.length]; _progressKey = 'cry'; return;
        }
      } catch (_) {}
    }
    final p = L10n.tList(isShort ? 'ep_msg_completed_short' : 'ep_msg_completed_long');
    _msg = p[widget.phraseSeed % p.length];
    _progressKey = isShort ? 'party' : 'chill';
  }

  void _triggerEffect() async {
    if (!_easterEggsEnabled) return;
    
    _spamCount++;
    _spamTimer?.cancel();
    _spamTimer = Timer(const Duration(seconds: 4), () {
      if (mounted) setState(() => _spamCount = 0);
    });

    setState(() => _isAnimatingText = true);
    final rnd = Random();
    
    if (_spamCount > 4) {
      await _dispatch(ScenarioGroup.spam, OutputType.toast, rnd);
      await Future.delayed(const Duration(seconds: 1));
      if (mounted) setState(() => _isAnimatingText = false);
      return;
    }
    if (_isAnimatingText && _spamCount <= 1) {
       // Allow animation reset
    }

    final roll = rnd.nextInt(100);
    if (roll == 0) {
      await _legendary();
    } else {
      ScenarioGroup grp;
      if (roll < 34) grp = ScenarioGroup.universal;
      else if (roll < 67) grp = _matchedGenres.isNotEmpty ? ScenarioGroup.genre : ScenarioGroup.universal;
      else grp = ScenarioGroup.progress;
      final outType = OutputType.values[rnd.nextInt(3)];
      await _dispatch(grp, outType, rnd);
    }
    await Future.delayed(const Duration(seconds: 3));
    if (mounted) setState(() => _isAnimatingText = false);
  }

  Future<void> _dispatch(ScenarioGroup grp, OutputType out, Random rnd) async {
    switch (grp) {
      case ScenarioGroup.universal: await _universalFx(out, rnd); break;
      case ScenarioGroup.genre:
        final g = _matchedGenres[rnd.nextInt(_matchedGenres.length)];
        await _genreFx(g, out, rnd); break;
      case ScenarioGroup.progress: await _progressFx(out, rnd); break;
      case ScenarioGroup.legendary: break;
      case ScenarioGroup.spam: await _spamFx(rnd); break;
    }
  }


  Future<void> _spamFx(Random rnd) async {
    final movieName = widget.movie?.name ?? L10n.t('this_movie');
    final rawJokes = L10n.tList('easter_spam_jokes');
    final jokes = rawJokes.isEmpty 
        ? ["Spam!"] 
        : rawJokes.map((j) => j.replaceAll('{MOVIE}', movieName)).toList();
    
    _progressKey = 'rage';
    _showToast([jokes[rnd.nextInt(jokes.length)]], rnd);
    
    if (mounted) setState(() {});
  }

  Future<void> _universalFx(OutputType out, Random rnd) async {
    final isMidnight = DateTime.now().hour < 4;
    if (isMidnight) {
      switch (out) {
        case OutputType.sticker:   _showLottie(_sleepStickers[rnd.nextInt(_sleepStickers.length)]); break;
        case OutputType.particles: _spawnParticles(_sleepParticles, rnd); break;
        case OutputType.toast:     _showToast(L10n.tList('easter_universal_midnight'), rnd); break;
      }
      return;
    }
    switch (out) {
      case OutputType.sticker:   _showLottie(_universalStickers[rnd.nextInt(_universalStickers.length)]); break;
      case OutputType.particles: _spawnParticles(_universalParticles, rnd); break;
      case OutputType.toast:     _showToast(L10n.tList('easter_universal'), rnd); break;
    }
  }

  Future<void> _genreFx(SupportedGenre g, OutputType out, Random rnd) async {
    switch (out) {
      case OutputType.sticker:
        final s = _genreStickers[g]!; _showLottie(s[rnd.nextInt(s.length)]); break;
      case OutputType.particles:
        _spawnParticles(_genreParticles[g]!, rnd); break;
      case OutputType.toast:
        _showToast(L10n.tList('easter_genre_${g.name}'), rnd); break;
    }
  }

  Future<void> _progressFx(OutputType out, Random rnd) async {
    final Map<String, List<String>> pp = {
      'party': ['\u{1F389}', '\u{1F38A}', '\u{1F386}', '\u2728', '\u{1F973}'],
      'cry':   ['\u{1F62D}', '\u{1F4A7}', '\u2764\uFE0F', '\u{1F9A7}', '\u{1F494}'],
      'rage':  ['\u{1F624}', '\u23F3', '\u{1F525}', '\u{1F4A2}', '\u{1F620}'],
      'chill': ['\u{1F60C}', '\u{1F375}', '\u{1F964}', '\u{1F37F}', '\u{1F338}'],
      'tense': ['\u{1F631}', '\u{1F62C}', '\u{1F4A3}', '\u26A1', '\u{1F514}'],
    };
    switch (out) {
      case OutputType.sticker:
        final s = _progressStickers[_progressKey] ?? _progressStickers['chill']!;
        _showLottie(s[rnd.nextInt(s.length)]); break;
      case OutputType.particles:
        _spawnParticles(pp[_progressKey] ?? pp['chill']!, rnd); break;
      case OutputType.toast:
        _showToast(L10n.tList('easter_progress_${_progressKey}'), rnd); break;
    }
    if (_progressKey == 'party') _confettiController.play();
  }

  Future<void> _legendary() async {
    _confettiController.play();
    if (!mounted) return;
    showDialog(
      context: context, 
      barrierColor: Colors.black54, 
      builder: (ctx) {
        Future.delayed(const Duration(milliseconds: 3500), () { 
          if (ctx.mounted && Navigator.of(ctx).canPop()) Navigator.of(ctx).pop(); 
        });
        return IgnorePointer(child: NextEpisodeTracker._buildLegendaryWidget());
      }
    );
  }

  Widget _buildGiantEmoji(String emoji) {
    return Center(
      child: Text(emoji, style: const TextStyle(fontSize: 120, decoration: TextDecoration.none))
          .animate(onPlay: (c) => c.repeat(reverse: true))
          .scale(duration: 600.ms, curve: Curves.elasticOut)
          .shake(hz: 4, offset: const Offset(4, 4)),
    );
  }

  Widget _fallbackSticker() {
    final emoji = ['💥', '😂', '😍', '😭', '😱', '🚀', '🌈'][Random().nextInt(7)];
    return _buildGiantEmoji(emoji);
  }

  void _showJumpscare() {
    if (!mounted) return;
    showDialog(
      context: context, 
      barrierColor: Colors.black,
      builder: (ctx) {
        Future.delayed(const Duration(milliseconds: 1500), () { 
          if (ctx.mounted && Navigator.of(ctx).canPop()) Navigator.of(ctx).pop(); 
        });
        return Center(
          child: IgnorePointer(
            child: const Text('👹', style: TextStyle(fontSize: 250, decoration: TextDecoration.none))
                .animate()
                .scale(begin: const Offset(0.1, 0.1), end: const Offset(2.0, 2.0), duration: 150.ms, curve: Curves.easeIn)
                .shake(hz: 20, offset: const Offset(15, 15))
                .tint(color: Colors.red, duration: 100.ms)
                .then(delay: 800.ms)
                .fadeOut(duration: 200.ms),
          ),
        );
      }
    );
  }

  void _showLottie(String url) {
    if (!mounted) return;
    
    if (url == 'JUMPSCARE') {
      _showJumpscare();
      return;
    }

    showDialog(context: context, barrierColor: Colors.transparent, builder: (ctx) {
      Future.delayed(const Duration(milliseconds: 2800), () { if (ctx.mounted && Navigator.of(ctx).canPop()) Navigator.of(ctx).pop(); });
      
      Widget contentWidget;
      if (url.endsWith('.json')) {
        contentWidget = url.startsWith('assets') 
            ? Lottie.asset(url, errorBuilder: (_, __, ___) => _fallbackSticker())
            : Lottie.network(url, errorBuilder: (_, __, ___) => _fallbackSticker());
      } else if (url.endsWith('.jpg') || url.endsWith('.png') || url.endsWith('.webp')) {
        contentWidget = (url.startsWith('http') ? Image.network(url) : Image.asset(url))
            .animate(onPlay: (c) => c.repeat(reverse: true))
            .scale(begin: const Offset(1,1), end: const Offset(1.1, 1.1), duration: 600.ms)
            .rotate(begin: -0.05, end: 0.05, duration: 600.ms);
      } else {
        contentWidget = _buildGiantEmoji(url);
      }
      
      return Center(
        child: IgnorePointer(
          child: SizedBox(
            width: 260,
            height: 260,
            child: contentWidget,
          ),
        ),
      );
    });
  }

  void _showToast(List<String> quotes, Random rnd) {
    if (quotes.isEmpty || !mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(quotes[rnd.nextInt(quotes.length)]), duration: const Duration(seconds: 3)));
  }

  void _spawnParticles(List<String> emojis, Random rnd) {
    if (!mounted) return;
    final overlay = Overlay.of(context);
    final size = MediaQuery.of(context).size;
    final fall = rnd.nextBool();
    final sy = fall ? -40.0 : size.height + 40;
    final ey = fall ? size.height + 40 : -40.0;
    for (int i = 0; i < 18; i++) {
      final sx = rnd.nextDouble() * size.width;
      final ex = sx + (rnd.nextDouble() - 0.5) * 120;
      final delay = rnd.nextInt(600);
      final dur = 1400 + rnd.nextInt(900);
      final emoji = emojis[rnd.nextInt(emojis.length)];
      late OverlayEntry entry;
      entry = OverlayEntry(builder: (ctx) => TweenAnimationBuilder<double>(
        tween: Tween(begin: 0, end: 1),
        duration: Duration(milliseconds: dur),
        builder: (_, v, __) {
          if (v >= 1) WidgetsBinding.instance.addPostFrameCallback((_) { if (entry.mounted) entry.remove(); });
          final op = (v < 0.15 ? v / 0.15 : (v > 0.8 ? (1 - v) / 0.2 : 1.0)).clamp(0.0, 1.0);
          return Positioned(left: sx + (ex-sx)*v, top: sy + (ey-sy)*v, child: Opacity(opacity: op, child: Text(emoji, style: const TextStyle(fontSize: 30, decoration: TextDecoration.none))));
        },
      ));
      Future.delayed(Duration(milliseconds: delay), () { if (mounted) overlay.insert(entry); });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_msg.isEmpty) return const SizedBox.shrink();
    Widget tw = Text(_msg, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w500, color: Colors.white, fontStyle: FontStyle.italic));
    if (_isAnimatingText && _easterEggsEnabled) {
      switch (_progressKey) {
        case 'party': tw = tw.animate().scale(duration: 200.ms).shimmer(duration: 800.ms, color: Colors.yellowAccent); break;
        case 'rage':  tw = tw.animate().shake(hz: 8, offset: const Offset(6, 0)).tint(color: Colors.redAccent, duration: 600.ms); break;
        case 'tense': tw = tw.animate().shimmer(duration: 600.ms, color: Colors.orangeAccent).shake(hz: 4, offset: const Offset(3, 0)); break;
        case 'cry':   tw = tw.animate().fade(duration: 400.ms).shimmer(duration: 1000.ms, color: Colors.blueAccent); break;
        default:      tw = tw.animate().shimmer(duration: 900.ms, color: Colors.white54).moveY(end: -3, duration: 300.ms);
      }
    }
    return Padding(
      padding: const EdgeInsets.only(top: 16),
      child: GestureDetector(
        onTap: _easterEggsEnabled ? _triggerEffect : null,
        child: MouseRegion(
          cursor: _easterEggsEnabled ? SystemMouseCursors.click : SystemMouseCursors.basic,
          child: Stack(clipBehavior: Clip.none, alignment: Alignment.center, children: [
            tw,
            Positioned(top: -20, child: ConfettiWidget(
              confettiController: _confettiController,
              blastDirectionality: BlastDirectionality.explosive,
              particleDrag: 0.05, emissionFrequency: 0.06, numberOfParticles: 35, gravity: 0.08,
              colors: const [Colors.green, Colors.blue, Colors.pink, Colors.orange, Colors.purple, Colors.yellow, Colors.red, Colors.cyan],
            )),
          ]),
        ),
      ),
    );
  }
}
