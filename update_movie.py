with open("lib/models/movie.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add totalEpisodes field
content = content.replace("final String currentEpisode;", "final String currentEpisode;\n  final String totalEpisodes;")
content = content.replace("required this.currentEpisode,", "required this.currentEpisode,\n    required this.totalEpisodes,")
content = content.replace("currentEpisode: json['current_episode'] ?? json['episode_current'] ?? '',", "currentEpisode: json['current_episode'] ?? json['episode_current'] ?? '',\n      totalEpisodes: json['total_episodes']?.toString() ?? json['episode_total']?.toString() ?? '',")
content = content.replace("String? currentEpisode,", "String? currentEpisode,\n    String? totalEpisodes,")
content = content.replace("currentEpisode: currentEpisode ?? this.currentEpisode,", "currentEpisode: currentEpisode ?? this.currentEpisode,\n      totalEpisodes: totalEpisodes ?? this.totalEpisodes,")

with open("lib/models/movie.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated movie.dart")
