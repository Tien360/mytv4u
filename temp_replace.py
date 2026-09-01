with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    c = f.read()

old_spam_fx = """  Future<void> _spamFx(Random rnd) async {
    final movieName = widget.movie?.name ?? 'Phim nÃ y';
    final spamJokes = [
      "Báº¥m gÃ¬ báº¥m nhiá» u tháº¿? Bá»™ tÃ­nh lÃ m hacker há»Ÿ?",
      "Báº¡n cÃ³ spam chÃ¡y cáº£ chuá»™t thÃ¬ phim cÅ©ng chÆ°a ra táº­p má»›i Ä‘Ã¢u!",
      "ThÆ¡ táº·ng báº¡n:\\n$movieName hay tháº­t lÃ  hay\\nNhÆ°ng mÃ  chÆ°a chiáº¿u, báº¥m hoÃ i Ä‘á»©t tay!",
      "TÃ´i lÃ  há»™p bÃ¡o lá»‹ch, khÃ´ng pháº£i mÃ¡y Ä‘áº» táº­p phim má»›i nha!",
      "Ä Ã£ báº£o lÃ  chÆ°a cÃ³ mÃ ! LÃ¬ xÃ¬ admin 50k Ä‘i rá»“i tÃ´i giá»¥c Ä‘áº¡o diá»…n cho.",
      "Háº¿t vÄƒn Ä‘á»ƒ trÃªu báº¡n rá»“i! Má» i tay chÆ°a? Táº¯t mÃ¡y Ä‘i ngá»§ Ä‘i!",
      "Báº¡n báº¥m nÃ¡t cÃ¡i nÃºt rá»“i kÃ¬a. Láº¡y chÃºa tÃ´i!",
      "Náº¿u báº¡n báº¥m thÃªm 100 láº§n ná»¯a, táº­p má»›i sáº½... váº«n khÃ´ng xuáº¥t hiá»‡n =))",
      "ThÆ¡ vá»  phim:\\n$movieName ká»‹ch tÃ­nh báº¥t ngá» \\nSpam hoÃ i Ä‘au ngÃ³n, tháº«n thá»  chá»  mong!",
      "Nghá»‹ch hoÃ i khÃ´ng chÃ¡n háº£ báº¡n gÃ¬ Æ¡i?",
      "Nháº¥p chuá»™t 10 láº§n 1 giÃ¢y... báº¡n chÆ¡i game MOBA cháº¯c pro láº¯m nhá»‰?",
      "Ä Ã£ báº£o lÃ  khÃ´ng cÃ³ gÃ¬ Ä‘Ã¢u mÃ  cá»© báº¥m! Ngoan, Ä‘i xem phim khÃ¡c Ä‘i."
    ];
    
    _progressKey = 'rage';
    _showToast([spamJokes[rnd.nextInt(spamJokes.length)]], rnd);
    // Vibrate text
    if (mounted) setState(() {});
  }"""

new_spam_fx = """  Future<void> _spamFx(Random rnd) async {
    final movieName = widget.movie?.name ?? (L10n.t('this_movie') ?? 'This movie');
    final rawJokes = L10n.tList('easter_spam_jokes');
    final jokes = rawJokes.isEmpty 
        ? ["Spam!"] 
        : rawJokes.map((j) => j.replaceAll('{MOVIE}', movieName)).toList();
    
    _progressKey = 'rage';
    _showToast([jokes[rnd.nextInt(jokes.length)]], rnd);
    
    if (mounted) setState(() {});
  }"""

# Python's replace might fail if encoding messes up the raw string in old_spam_fx.
# Let's use substring finding
start_idx = c.find("  Future<void> _spamFx(Random rnd) async {")
end_idx = c.find("  Future<void> _universalFx", start_idx)

if start_idx != -1 and end_idx != -1:
    c = c[:start_idx] + new_spam_fx + "\n\n" + c[end_idx:]
    with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
        f.write(c)
    print("Replaced _spamFx with L10n")
else:
    print("Could not find _spamFx bounds")
