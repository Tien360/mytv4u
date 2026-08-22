import 'dart:async';
import 'package:mytv4u_flutter/api/phim_api.dart';
import 'package:mytv4u_flutter/models/movie.dart';

void main() async {
  print('Searching...');
  final movies = await PhimApi.searchMovies('minions và quái vật');
  Movie? match;
  for (var m in movies) {
    if (m.originalName == 'Minions & Monsters') {
      match = m;
      print('Found match! slugs: \');
      break;
    }
  }

  if (match != null) {
    print('Fetching details for \...');
    final stream = PhimApi.fetchMovieDetailStream(match.slug, initialMovie: match);
    await for (var m in stream) {
      print('Stream emitted! sources: \');
      for (var srv in m.episodes) {
        print(' - \: \ items');
      }
    }
  }
}
