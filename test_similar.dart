import 'dart:convert';
import 'package:http/http.dart' as http;

class Movie {
  final String originalName;
  final String year;
  Movie(this.originalName, this.year);
}

bool _isSimilarMovieGlobal(Movie? initial, Movie fetched) {
    if (initial == null) return true;
    if (initial.originalName.isNotEmpty && fetched.originalName.isNotEmpty) {
      String normA = initial.originalName.toLowerCase().replaceAll(
        RegExp(r'[^a-z0-9]'),
        '',
      );
      String normB = fetched.originalName.toLowerCase().replaceAll(
        RegExp(r'[^a-z0-9]'),
        '',
      );
      print('normA: \, normB: \');
      if (normA != normB && !normA.contains(normB) && !normB.contains(normA)) {
        return false;
      }
    }
    print('yearA: \, yearB: \');
    if (initial.year.isNotEmpty &&
        fetched.year.isNotEmpty &&
        initial.year != fetched.year) {
      return false;
    }
    return true;
}

void main() {
  Movie initial = Movie('Minions & Monsters', '2026');
  Movie fetched = Movie('Minions & Monsters', '2026');
  print(_isSimilarMovieGlobal(initial, fetched));
}
