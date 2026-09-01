with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Add _isCompletedMode
c = c.replace("  int _spamCount = 0;", "  bool _isCompletedMode = false;\n  int _spamCount = 0;")

# 2. Update _airingState and _completedState
c = c.replace("  void _airingState(", "  void _airingState(\n    _isCompletedMode = false;")
c = c.replace("void _completedState(", "void _completedState(\n    _isCompletedMode = true;")

# 3. Update _spamFx
old_spam = """  Future<void> _spamFx(Random rnd) async {
    final movieName = widget.movie?.name ?? L10n.t('this_movie');
    final rawJokes = L10n.tList('easter_spam_jokes');
    final jokes = rawJokes.isEmpty 
        ? ["Spam!"] 
        : rawJokes.map((j) => j.replaceAll('{MOVIE}', movieName)).toList();"""

new_spam = """  Future<void> _spamFx(Random rnd) async {
    final movieName = widget.movie?.name ?? L10n.t('this_movie');
    final l10nKey = _isCompletedMode ? 'easter_spam_jokes_completed' : 'easter_spam_jokes';
    final rawJokes = L10n.tList(l10nKey);
    final jokes = rawJokes.isEmpty 
        ? ["Spam!"] 
        : rawJokes.map((j) => j.replaceAll('{MOVIE}', movieName)).toList();"""

c = c.replace(old_spam, new_spam)

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated dart code")
