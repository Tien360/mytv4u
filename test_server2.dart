import 'dart:io';

void main() {
  var uriStr = "/tiktok/foo?bar=1&x=2";
  var realUrl = 'https://p19-ad-site-sign-sg.tiktokcdn.com/' + uriStr.substring(8);
  print(realUrl);
}
