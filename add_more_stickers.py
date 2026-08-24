import re

with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Replace _genreStickers
old_stickers = """  const Map<SupportedGenre, List<String>> _genreStickers = {
    SupportedGenre.action:        ['assets/lottie/lf20_fyye8szy.json', 'https://assets5.lottiefiles.com/packages/lf20_obhph3t0.json', 'https://assets2.lottiefiles.com/packages/lf20_dmxakyf0.json'],
    SupportedGenre.romance:       ['https://assets9.lottiefiles.com/packages/lf20_ksafzlmf.json', 'assets/lottie/lf20_qp1q7mct.json', 'assets/lottie/lf20_ydo1amjm.json'],
    SupportedGenre.comedy:        ['https://assets1.lottiefiles.com/packages/lf20_tclbbmku.json', 'https://assets3.lottiefiles.com/packages/lf20_yj7korxa.json', 'https://assets7.lottiefiles.com/packages/lf20_b8ixs0qm.json'],
    SupportedGenre.historical:    ['assets/lottie/lf20_ofa3xwo7.json', 'assets/lottie/lf20_3rqwsqnj.json'],
    SupportedGenre.psychological: ['https://assets6.lottiefiles.com/packages/lf20_uw0knnbz.json', 'assets/lottie/lf20_aZTdD5.json'],
    SupportedGenre.crime:         ['assets/lottie/lf20_5tl1xxnz.json', 'assets/lottie/lf20_kkflmtur.json'],
    SupportedGenre.scifi:         ['assets/lottie/lf20_khzniaya.json', 'https://assets8.lottiefiles.com/packages/lf20_oqyiaqx4.json', 'assets/lottie/lf20_syqnfe7c.json'],
    SupportedGenre.horror:        ['assets/lottie/lf20_m9zragkd.json', 'https://assets10.lottiefiles.com/packages/lf20_pKiaWt.json', 'https://assets6.lottiefiles.com/packages/lf20_uxzqnknw.json'],
    SupportedGenre.animation:     ['https://assets3.lottiefiles.com/packages/lf20_jbb4x5qp.json', 'assets/lottie/lf20_touohxv0.json', 'assets/lottie/lf20_xlmz9xwm.json'],
    SupportedGenre.lgbt:          ['https://assets9.lottiefiles.com/packages/lf20_7ysabwid.json', 'https://assets5.lottiefiles.com/packages/lf20_ksafzlmf.json'],
  };

  const Map<String, List<String>> _progressStickers = {
    'party': ['https://assets4.lottiefiles.com/packages/lf20_touohxv0.json', 'https://assets5.lottiefiles.com/packages/lf20_dvd9mxbe.json', 'https://assets6.lottiefiles.com/packages/lf20_b8ixs0qm.json'],
    'cry':   ['https://assets2.lottiefiles.com/packages/lf20_ydo1amjm.json', 'https://assets3.lottiefiles.com/packages/lf20_obhph3t0.json', 'assets/lottie/lf20_qp1q7mct.json'],
    'rage':  ['https://assets5.lottiefiles.com/packages/lf20_obhph3t0.json', 'assets/lottie/lf20_5tl1xxnz.json', 'assets/lottie/lf20_syqnfe7c.json'],
    'chill': ['https://assets8.lottiefiles.com/packages/lf20_oqyiaqx4.json', 'https://assets1.lottiefiles.com/packages/lf20_yrtouvgn.json'],
    'tense': ['assets/lottie/lf20_m9zragkd.json', 'https://assets10.lottiefiles.com/packages/lf20_pKiaWt.json'],
  };"""

new_stickers = """  const Map<SupportedGenre, List<String>> _genreStickers = {
    SupportedGenre.action:        ['assets/lottie/lf20_fyye8szy.json', '💥', '💣', '🔥', '🥊', '🏍️', '🔫'],
    SupportedGenre.romance:       ['assets/lottie/lf20_qp1q7mct.json', 'assets/lottie/lf20_ydo1amjm.json', '💖', '🥰', '💘', '💍', '💏', '🌹'],
    SupportedGenre.comedy:        ['😂', '🤣', '🤪', '🤡', '😆', '🙊'],
    SupportedGenre.historical:    ['assets/lottie/lf20_ofa3xwo7.json', 'assets/lottie/lf20_3rqwsqnj.json', '⛩️', '🗡️', '🏯', '📜', '🎎'],
    SupportedGenre.psychological: ['assets/lottie/lf20_aZTdD5.json', '🧠', '😵‍💫', '🎭', '🌀', '👁️'],
    SupportedGenre.crime:         ['assets/lottie/lf20_5tl1xxnz.json', 'assets/lottie/lf20_kkflmtur.json', '🕵️', '🚓', '🩸', '🔪', '🔍'],
    SupportedGenre.scifi:         ['assets/lottie/lf20_khzniaya.json', 'assets/lottie/lf20_syqnfe7c.json', '🚀', '👽', '🤖', '🛸', '🌌'],
    SupportedGenre.horror:        ['assets/lottie/lf20_m9zragkd.json', '👻', '💀', '🧟', '🎃', '🧛', '🔪'],
    SupportedGenre.animation:     ['assets/lottie/lf20_touohxv0.json', 'assets/lottie/lf20_xlmz9xwm.json', '🦄', '🌈', '🧸', '🎈', '🪄'],
    SupportedGenre.lgbt:          ['🏳️‍🌈', '👨‍❤️‍👨', '👩‍❤️‍👩', '👬', '👭', '🦄'],
  };

  const Map<String, List<String>> _progressStickers = {
    'party': ['🎉', '🎊', '🥂', '🥳', '🎁', '💃'],
    'cry':   ['assets/lottie/lf20_qp1q7mct.json', '😭', '💔', '🥀', '☔', '😢'],
    'rage':  ['assets/lottie/lf20_5tl1xxnz.json', 'assets/lottie/lf20_syqnfe7c.json', '🤬', '🌋', '💢', '😠'],
    'chill': ['🍿', '🥤', '🛋️', '☕', '🎧', '🧘'],
    'tense': ['assets/lottie/lf20_m9zragkd.json', '😱', '😰', '🥶', '👀', '⏳'],
  };"""

# Use regex to replace to avoid exact whitespace issues
text = re.sub(r'const Map<SupportedGenre, List<String>> _genreStickers = \{.*?\};', new_stickers, text, flags=re.DOTALL)


# 2. Update _showLottie and _fallbackSticker
old_show = """  Widget _fallbackSticker() {
    final emoji = ['💥', '😂', '😍', '😭', '😱', '🚀', '🌈'][Random().nextInt(7)];
    return Text(emoji, style: const TextStyle(fontSize: 120, decoration: TextDecoration.none))
        .animate(onPlay: (c) => c.repeat(reverse: true))
        .scale(duration: 500.ms, curve: Curves.elasticOut)
        .shake(hz: 3, offset: const Offset(5, 5));
  }

  void _showLottie(String url) {
    if (!mounted) return;
    showDialog(context: context, barrierColor: Colors.transparent, builder: (ctx) {
      Future.delayed(const Duration(milliseconds: 2800), () { if (ctx.mounted && Navigator.of(ctx).canPop()) Navigator.of(ctx).pop(); });
      return Center(
        child: IgnorePointer(
          child: SizedBox(
            width: 260,
            height: 260,
            child: url.startsWith('assets') 
                ? Lottie.asset(url, errorBuilder: (_, __, ___) => _fallbackSticker())
                : Lottie.network(url, errorBuilder: (_, __, ___) => _fallbackSticker()),
          ),
        ),
      );
    });
  }"""

new_show = """  Widget _buildGiantEmoji(String emoji) {
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

  void _showLottie(String url) {
    if (!mounted) return;
    showDialog(context: context, barrierColor: Colors.transparent, builder: (ctx) {
      Future.delayed(const Duration(milliseconds: 2800), () { if (ctx.mounted && Navigator.of(ctx).canPop()) Navigator.of(ctx).pop(); });
      
      Widget contentWidget;
      if (url.endsWith('.json')) {
        contentWidget = url.startsWith('assets') 
            ? Lottie.asset(url, errorBuilder: (_, __, ___) => _fallbackSticker())
            : Lottie.network(url, errorBuilder: (_, __, ___) => _fallbackSticker());
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
  }"""

if "Widget _fallbackSticker()" in text:
    text = text.replace(old_show, new_show)

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Added massive emoji sticker pool!")
