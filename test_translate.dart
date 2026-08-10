import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final text = 'Xin chào thế giới, hôm nay bạn thế nào?';
  final url = Uri.parse('https://translate.googleapis.com/translate_a/single?client=gtx&sl=vi&tl=en&dt=t&q=\');
  final res = await http.get(url);
  final jsonList = json.decode(res.body);
  final translated = jsonList[0][0][0];
  print(translated);
}
