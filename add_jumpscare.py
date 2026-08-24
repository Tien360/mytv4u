import re

with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update horror genre to include JUMPSCARE
text = text.replace(
    "'assets/lottie/lf20_m9zragkd.json', '👻', '💀', '🧟', '🎃', '🧛', '🔪'",
    "'assets/lottie/lf20_m9zragkd.json', '👻', '💀', '🧟', '🎃', '🧛', '🔪', 'JUMPSCARE'"
)

# 2. Update chill progress to include popcorn.jpg
text = text.replace(
    "'🍿', '🥤', '🛋️', '☕', '🎧', '🧘'",
    "'assets/easter/popcorn.jpg', '🍿', '🥤', '🛋️', '☕', '🎧', '🧘'"
)

# 3. Update _showLottie (rename to _showSticker internally but keep name same to avoid refactor)
old_show = """  void _showLottie(String url) {
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

new_show = """  void _showJumpscare() {
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
      } else if (url.endsWith('.jpg') || url.endsWith('.png')) {
        contentWidget = Image.asset(url)
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
  }"""

if "void _showLottie" in text:
    text = text.replace(old_show, new_show)

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Added JUMPSCARE and popcorn image!")
