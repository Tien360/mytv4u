import re

with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Replace triggerLegendaryFromOutside
old_trigger = """  static void triggerLegendaryFromOutside(BuildContext context) {
    final overlay = Overlay.of(context);
    late OverlayEntry entry;
    entry = OverlayEntry(builder: (ctx) {
      Future.delayed(const Duration(milliseconds: 3200), () { if (entry.mounted) entry.remove(); });
      return Positioned.fill(child: IgnorePointer(child: Center(child: _legendarySticker.startsWith('assets') ? Lottie.asset(_legendarySticker, width: 300, height: 300) : Lottie.network(_legendarySticker, width: 300, height: 300))));
    });
    overlay.insert(entry);
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text(L10n.currentLang == 'vi' ? 'Cảm ơn bạn đã đồng hành cùng ứng dụng MyTV4U ❤️' : 'Thank you for being with MyTV4U App ❤️'),
      duration: const Duration(seconds: 4),
      backgroundColor: Colors.amber.shade800,
    ));
  }"""

new_trigger = """  static Widget _buildLegendaryWidget() {
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
  }"""

text = text.replace(old_trigger, new_trigger)

# 2. Replace _legendary
old_leg = """  Future<void> _legendary() async {
    _confettiController.play();
    _showLottie(_legendarySticker);
    await Future.delayed(const Duration(milliseconds: 400));
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(L10n.currentLang == 'vi' ? 'Cảm ơn bạn đã đồng hành cùng ứng dụng MyTV4U ❤️' : 'Thank you for being with MyTV4U App ❤️'),
        duration: const Duration(seconds: 4),
        backgroundColor: Colors.amber.shade800,
      ));
    }
  }"""

new_leg = """  Future<void> _legendary() async {
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
  }"""

text = text.replace(old_leg, new_leg)

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated Legendary Group 4")
