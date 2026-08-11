import 'dart:io';

class SystemUtils {
  static int _totalRamBytes = -1;

  static Future<void> initAsync() async {
    if (Platform.isWindows) {
      try {
        final result = await Process.run('wmic', ['OS', 'get', 'TotalVisibleMemorySize', '/Value']);
        if (result.exitCode == 0) {
          final output = result.stdout.toString().trim();
          final RegExp regExp = RegExp(r'TotalVisibleMemorySize=(\d+)');
          final match = regExp.firstMatch(output);
          if (match != null) {
            final kb = int.tryParse(match.group(1)!);
            if (kb != null) {
              _totalRamBytes = kb * 1024;
            }
          }
        }
      } catch (_) {
        // Ignore error
      }
    }
  }

  /// Tính toán dung lượng bộ nhớ đệm ảnh (Image Cache) cho Flutter dựa trên RAM
  static int getOptimalImageCacheSizeMB() {
    if (_totalRamBytes <= 0) {
      return 100; // Mặc định 100MB
    }
    
    final gb = _totalRamBytes / (1024 * 1024 * 1024);
    
    if (gb >= 31.0) {
      return 1024; // 1GB cache ảnh cho máy >= 32GB RAM
    } else if (gb >= 15.0) {
      return 512; // 512MB cache ảnh cho máy >= 16GB RAM
    } else if (gb >= 7.0) {
      return 256; // 256MB cache ảnh cho máy >= 8GB RAM
    } else if (gb >= 3.5) {
      return 100; // 100MB cache ảnh cho máy >= 4GB RAM
    } else {
      return 50; // 50MB cho máy < 4GB RAM
    }
  }

  /// Tính toán dung lượng RAM dành cho bộ đệm video dựa trên tổng RAM hệ thống
  static int getOptimalBufferSize() {
    if (_totalRamBytes <= 0) {
      return 128 * 1024 * 1024; // Mặc định 128MB nếu không lấy được thông tin
    }
    
    // Đổi ra GB (làm tròn số thập phân)
    final gb = _totalRamBytes / (1024 * 1024 * 1024);
    
    if (gb >= 15.0) {
      return 1024 * 1024 * 1024; // 1GB buffer cho máy >= 16GB RAM
    } else if (gb >= 7.0) {
      return 512 * 1024 * 1024; // 512MB buffer cho máy >= 8GB RAM
    } else if (gb >= 3.5) {
      return 256 * 1024 * 1024; // 256MB buffer cho máy >= 4GB RAM
    } else {
      return 128 * 1024 * 1024; // 128MB cho máy < 4GB RAM
    }
  }
}
