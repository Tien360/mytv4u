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
class LivescoreMatch {
  final String time;
  final String teamHome;
  final String score;
  final String teamAway;
  final String status;

  LivescoreMatch({
    required this.time,
    required this.teamHome,
    required this.score,
    required this.teamAway,
    required this.status,
  });

  factory LivescoreMatch.fromJson(Map<String, dynamic> json) {
    return LivescoreMatch(
      time: json['time'] ?? '',
      teamHome: json['team_home'] ?? '',
      score: json['score'] ?? 'vs',
      teamAway: json['team_away'] ?? '',
      status: json['status'] ?? '',
    );
  }
}

class LivescoreDay {
  final String date;
  final List<LivescoreMatch> matches;

  LivescoreDay({
    required this.date,
    required this.matches,
  });

  factory LivescoreDay.fromJson(Map<String, dynamic> json) {
    var list = json['matches'] as List? ?? [];
    List<LivescoreMatch> matchList = list.map((i) => LivescoreMatch.fromJson(i)).toList();
    return LivescoreDay(
      date: json['date'] ?? '',
      matches: matchList,
    );
  }
}

class LivescoreLeague {
  final String leagueName;
  final List<LivescoreDay> days;

  LivescoreLeague({
    required this.leagueName,
    required this.days,
  });

  factory LivescoreLeague.fromJson(Map<String, dynamic> json) {
    var list = json['days'] as List? ?? [];
    List<LivescoreDay> dayList = list.map((i) => LivescoreDay.fromJson(i)).toList();
    return LivescoreLeague(
      leagueName: json['league_name'] ?? '',
      days: dayList,
    );
  }
}

class LivescoreData {
  final String lastUpdate;
  final List<LivescoreLeague> leagues;

  LivescoreData({
    required this.lastUpdate,
    required this.leagues,
  });

  factory LivescoreData.fromJson(Map<String, dynamic> json) {
    var list = json['leagues'] as List? ?? [];
    List<LivescoreLeague> leagueList = list.map((i) => LivescoreLeague.fromJson(i)).toList();
    return LivescoreData(
      lastUpdate: json['last_update'] ?? '',
      leagues: leagueList,
    );
  }
}
