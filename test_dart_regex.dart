void main() {
  final html = '"videoRenderer":{"videoId":"XtpMWvBnNmQ"';
  final regex1 = RegExp(r'\"videoRenderer\":\{\"videoId\":\"([a-zA-Z0-9_-]{11})\"');
  final regex2 = RegExp(r'"videoRenderer":\{"videoId":"([a-zA-Z0-9_-]{11})"');
  
  print("Regex 1 match: ${regex1.firstMatch(html)?.group(1)}");
  print("Regex 2 match: ${regex2.firstMatch(html)?.group(1)}");
}
