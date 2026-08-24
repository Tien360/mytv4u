import re

with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

old_func = """  void _showLottie(String url) {
    if (!mounted) return;
    showDialog(context: context, barrierColor: Colors.transparent, builder: (ctx) {
      Future.delayed(const Duration(milliseconds: 2800), () { if (ctx.mounted && Navigator.of(ctx).canPop()) Navigator.of(ctx).pop(); });
      return Center(child: IgnorePointer(child: SizedBox(width: 260, height: 260, child: Lottie.network(url, errorBuilder: (_, __, ___) => const SizedBox()))));
    });
  }"""

new_func = """  Widget _fallbackSticker() {
    final emoji = ['💥', '😂', '😍', '😭', '😱', '🚀', '🌈'][Random().nextInt(7)];
    return Text(emoji, style: const TextStyle(fontSize: 120, decoration: TextDecoration.none))
        .animate(onPlay: (c) => c.repeat(reverse: true))
        .scale(duration: 500.ms, curve: Curves.elasticOut)
        .shake(hz: 3, amount: 5);
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

if "void _showLottie" in text:
    text = text.replace(old_func, new_func)

# Also fix the legendary sticker in triggerLegendaryFromOutside
old_leg = "child: Lottie.network(_legendarySticker, width: 300, height: 300, errorBuilder: (_, __, ___) => const SizedBox())"
new_leg = "child: _legendarySticker.startsWith('assets') ? Lottie.asset(_legendarySticker, width: 300, height: 300) : Lottie.network(_legendarySticker, width: 300, height: 300)"
text = text.replace(old_leg, new_leg)

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated _showLottie!")
