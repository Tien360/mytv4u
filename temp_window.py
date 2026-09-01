with open("lib/main.dart", "r", encoding="utf-8") as f:
    c = f.read()

listener_code = """
class AppWindowListener extends WindowListener {
  @override
  void onWindowClose() async {
    // Kill stremio server and backend processes
    StremioServer.stop();
    // Destroy window and force exit to instantly kill Webview and Audio
    await windowManager.destroy();
    exit(0);
  }
}
"""

c = c.replace("class MyTV4UApp extends", listener_code + "\nclass MyTV4UApp extends")

init_code = """  await windowManager.ensureInitialized();
  
  WindowOptions windowOptions = const WindowOptions("""

new_init_code = """  await windowManager.ensureInitialized();
  await windowManager.setPreventClose(true);
  windowManager.addListener(AppWindowListener());
  
  WindowOptions windowOptions = const WindowOptions("""

c = c.replace(init_code, new_init_code)

with open("lib/main.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated main.dart with AppWindowListener!")
