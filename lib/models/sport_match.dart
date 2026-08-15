class SportSource {
  final String name;
  final String link;
  final String logo;

  SportSource({
    required this.name,
    required this.link,
    required this.logo,
  });

  factory SportSource.fromJson(Map<String, dynamic> json) {
    return SportSource(
      name: json['name'] ?? 'Server',
      link: json['link'] ?? '',
      logo: json['logo'] ?? '',
    );
  }
}

class SportMatch {
  final String id;
  final String title;
  final String time;
  final String league;
  final String status;
  final List<SportSource> sources;

  SportMatch({
    required this.id,
    required this.title,
    required this.time,
    required this.league,
    required this.status,
    required this.sources,
  });
}
