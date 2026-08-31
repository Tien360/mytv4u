import 'package:file_picker/file_picker.dart';
void main() async {
  var x = await FilePicker.platform.pickFiles();
  print(x.runtimeType);
}
