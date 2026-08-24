import re

with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

old_leg_widget = """  static Widget _buildLegendaryWidget() {
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
  }"""

new_leg_widget = """  static Widget _buildLegendaryWidget() {
    return Center(
      child: Material(
        color: Colors.transparent,
        child: Stack(
          alignment: Alignment.center,
          children: [
            // Pháo hoa / party lottie phía sau
            Positioned(
              top: -50,
              child: Lottie.asset('assets/lottie/lf20_touohxv0.json', width: 400, height: 400, fit: BoxFit.cover, repeat: false)
                  .animate().fade(duration: 400.ms),
            ),
            Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Sticker Zalo siêu mượt (Google Noto Lottie)
                Lottie.asset('assets/lottie/noto_1f64f.json', width: 200, height: 200)
                    .animate(onPlay: (c) => c.repeat(reverse: true))
                    .scale(begin: const Offset(1, 1), end: const Offset(1.1, 1.1), duration: 800.ms, curve: Curves.easeInOut)
                    .moveY(begin: 0, end: -15, duration: 800.ms, curve: Curves.easeInOut),
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
          ],
        ),
      ),
    );
  }"""

text = text.replace(old_leg_widget, new_leg_widget)

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated legendary widget!")
