with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("void _airingState(\n    _isCompletedMode = false;Map<String, dynamic> nep", "void _airingState(Map<String, dynamic> nep")
c = c.replace("void _completedState(\n    _isCompletedMode = true;Map<String, dynamic> tmdb", "void _completedState(Map<String, dynamic> tmdb")

c = c.replace("final season = nep['season_number'] ?? 1;", "final season = nep['season_number'] ?? 1;\n    _isCompletedMode = false;")
c = c.replace("final total = tmdb['number_of_episodes'] ?? int.tryParse(widget.movie!.totalEpisodes) ?? 0;", "_isCompletedMode = true;\n    final total = tmdb['number_of_episodes'] ?? int.tryParse(widget.movie!.totalEpisodes) ?? 0;")

with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed syntax")
