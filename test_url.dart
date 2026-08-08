void main() {
  String url = 'https://v7.kkphimplayer7.com/20260717/0nWcndTd/index.m3u8';
  bool isWebview = url.startsWith('http') && 
      (url.contains('embed') || 
       url.contains('player') || 
       url.contains('iframe'));
  print(isWebview);
}
