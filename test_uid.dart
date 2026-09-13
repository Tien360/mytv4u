import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:io';

void main() async {
  final uid = 'Asus'; // wait, what is uid?
  final file = File(r'C:\Users\Asus\AppData\Roaming\MyTV4U\shared_preferences.json');
  if (file.existsSync()) {
     print(file.readAsStringSync());
  }
}
