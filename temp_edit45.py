import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

old_did_update = """  @override
  void didUpdateWidget(covariant HoverEpisodeButton oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.progress != oldWidget.progress || widget.episodeKey != oldWidget.episodeKey) {
      _localProgress = widget.progress;
      _loadDirectProgress();
    }
  }"""

new_did_update = """  @override
  void didUpdateWidget(covariant HoverEpisodeButton oldWidget) {
    super.didUpdateWidget(oldWidget);
    // Always reload because the parent might have called setState after returning from PlayerScreen
    // where the underlying SharedPreferences data changed but the widget properties (keys) didn't.
    _localProgress = widget.progress;
    _loadDirectProgress();
  }"""

c = c.replace(old_did_update, new_did_update)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated didUpdateWidget")
