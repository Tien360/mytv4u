import 'dart:io';

void main() {
  var file = File('lib/api/torrentio_api.dart');
  var text = file.readAsStringSync();
  text = text.replaceAll('ph?n', 'phần');
  file.writeAsStringSync(text);

  file = File('lib/api/phim_api.dart');
  text = file.readAsStringSync();
  text = text.replaceAll('ph?n', 'phần');
  file.writeAsStringSync(text);
  
  print('Fixed ph?n typo in both files!');
}
