import 'dart:io';

class HardwareInfo {
  static Future<int> getSystemRamMB() async {
    if (!Platform.isWindows) {
      return 4096;
    }
    try {
      final result = await Process.run('wmic', ['OS', 'get', 'TotalVisibleMemorySize', '/Value']);
      final output = result.stdout.toString();
      final match = RegExp(r'TotalVisibleMemorySize=(\d+)').firstMatch(output);
      if (match != null) {
        final ramKB = int.parse(match.group(1)!);
        return ramKB ~/ 1024;
      }
    } catch (e) {
      print('Error getting RAM: ' + e.toString());
    }
    return 4096;
  }
  static Future<int> getFreeSystemRamMB() async {
    if (!Platform.isWindows) {
      return 2048;
    }
    try {
      final result = await Process.run('wmic', ['OS', 'get', 'FreePhysicalMemory', '/Value']);
      final output = result.stdout.toString();
      final match = RegExp(r'FreePhysicalMemory=(\d+)').firstMatch(output);
      if (match != null) {
        final ramKB = int.parse(match.group(1)!);
        return ramKB ~/ 1024;
      }
    } catch (e) {
      print('Error getting Free RAM: ' + e.toString());
    }
    return 2048;
  }
}

