with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re
old_block = """onPressed: () async {
                    // Hiển thị dialog đang tải
                    showDialog(
                      context: context,
                      barrierDismissible: false,
                      builder: (_) =>
                          Center(child: CircularProgressIndicator()),
                    );

                    final updateInfo = await UpdateApi.checkForUpdate();

                    if (mounted) {
                      Navigator.of(context).pop(); // Đóng loading

                      if (updateInfo != null) {
                        showDialog(
                          context: context,
                          barrierDismissible: !updateInfo.isForceUpdate,
                          builder: (context) =>
                              UpdateDialog(updateInfo: updateInfo),
                        );
                      } else {
                        UIUtils.showCustomSnackBar(
                          context,
                          L10n.t('using_latest_version'),
                        );
                      }
                    }
                  }"""

new_block = """onPressed: () async {
                    final Uri url = Uri.parse('https://mytv4u.web.app/download');
                    if (await canLaunchUrl(url)) {
                      await launchUrl(url);
                    }
                  }"""
                  
c = c.replace(old_block, new_block)

# Add import if missing
if 'package:url_launcher/url_launcher.dart' not in c:
    c = "import 'package:url_launcher/url_launcher.dart';\n" + c

with open("lib/screens/settings_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated settings_screen.dart")
