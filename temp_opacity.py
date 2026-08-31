for file in ["lib/screens/movie_detail_screen.dart", "lib/screens/movie_detail_screen_test.dart"]:
    with open(file, "r", encoding="utf-8") as f:
        c = f.read()
    
    c = c.replace(
        """child: Offstage(
                            offstage: !_showInlineTrailer,
                            child: Webview(_webviewController),
                          ),""",
        """child: IgnorePointer(
                            ignoring: !_showInlineTrailer,
                            child: Opacity(
                              opacity: _showInlineTrailer ? 1.0 : 0.0,
                              child: Webview(_webviewController),
                            ),
                          ),"""
    )
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(c)

print("Changed Offstage to Opacity")
