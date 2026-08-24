import 'package:flutter/material.dart';

void main() {
  final budget = 85000000;
  final revenue = 493566930;
  final value = (budget / revenue).clamp(0.0, 1.0);
  print(value);
}
