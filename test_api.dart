
import 'package:flutter/material.dart';
import 'lib/api/phim_api.dart';
import 'lib/models/movie.dart';

void main() async {
  Movie movie = Movie(
    id: 'silo',
    name: 'Silo Phần 1',
    originName: 'Silo',
    thumbUrl: '',
    posterUrl: '',
    year: 2023,
    type: 'series',
  );
  final ytKey = await PhimApi.getTrailerStreamUrl(movie, true);
  print('YTKEY: $ytKey');
}
