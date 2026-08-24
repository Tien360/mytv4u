import 'dart:mirrors';
import 'package:media_kit/media_kit.dart';
void main() {
  ClassMirror classMirror = reflectClass(AudioTrack);
  classMirror.declarations.forEach((k, v) {
    if (v is VariableMirror) {
      print(MirrorSystem.getName(k));
    }
  });
}
