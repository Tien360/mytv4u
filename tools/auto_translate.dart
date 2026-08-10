import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<void> autoTranslate() async {
  print('[0/6] Đang đồng bộ và dịch tự động ngôn ngữ (i18n)...');
  final viFile = File('assets/langs/vi.json');
  final enFile = File('assets/langs/en.json');
  
  if (!viFile.existsSync()) return;
  
  Map<String, dynamic> viData = json.decode(viFile.readAsStringSync());
  Map<String, dynamic> enData = {};
  if (enFile.existsSync()) {
    enData = json.decode(enFile.readAsStringSync());
  }

  bool hasChanges = false;

  for (var key in viData.keys) {
    if (!enData.containsKey(key)) {
      final textVi = viData[key];
      print('  -> Đang dịch: "$textVi"');
      
      try {
        final url = Uri.parse('https://translate.googleapis.com/translate_a/single?client=gtx&sl=vi&tl=en&dt=t&q=${Uri.encodeComponent(textVi)}');
        final res = await http.get(url);
        if (res.statusCode == 200) {
          final jsonList = json.decode(res.body);
          String translatedText = '';
          for (var chunk in jsonList[0]) {
            translatedText += chunk[0];
          }
          enData[key] = translatedText;
          print('     => "$translatedText"');
          hasChanges = true;
        }
      } catch (e) {
        print('  -> Lỗi dịch: $e');
      }
    }
  }

  if (hasChanges) {
    enFile.writeAsStringSync(const JsonEncoder.withIndent('  ').convert(enData));
    print('  -> Đã lưu en.json!');
  } else {
    print('  -> Không có từ mới nào cần dịch.');
  }
}


void main() async {
  await autoTranslate();
}
