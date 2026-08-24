import re

with open("lib/screens/splash_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

new_dialog = """      showDialog(
        context: context,
        barrierDismissible: false,
        barrierColor: Colors.black.withValues(alpha: 0.8),
        builder: (context) => WillPopScope(
          onWillPop: () async => false, // Chặn nút back
          child: Dialog(
            backgroundColor: Colors.transparent,
            elevation: 0,
            child: GlassContainer(
              width: 400,
              padding: const EdgeInsets.all(24),
              borderRadius: 24,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline, color: Colors.redAccent, size: 48),
                  const SizedBox(height: 16),
                  Text(
                    L10n.t('app_disabled'),
                    style: const TextStyle(color: Colors.redAccent, fontSize: 20, fontWeight: FontWeight.bold),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    status['killMessage'] ?? L10n.t('contact_developer'),
                    style: const TextStyle(color: Colors.white70, fontSize: 16),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 32),
                  ElevatedButton(
                    onPressed: () => exit(0),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.redAccent,
                      padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: Text(
                      L10n.t('exit_app'),
                      style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      );"""

text = re.sub(r'      showDialog\(\n        context: context,\n        barrierDismissible: false,\n        builder: \(context\) => WillPopScope\(\n          onWillPop: \(\) async => false, // Chặn nút back\n          child: AlertDialog\(.*?\n          \),\n        \),\n      \);', new_dialog, text, flags=re.DOTALL)
with open("lib/screens/splash_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Replaced dialog in splash_screen!")
