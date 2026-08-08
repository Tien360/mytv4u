import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'package:package_info_plus/package_info_plus.dart';
import '../models/update_info.dart';
import 'firebase_api.dart';

class UpdateApi {
  static const String updateDocUrl = '${FirebaseApi.baseUrl}/updates/latest';
  static final Dio _dio = Dio();

  /// Kiểm tra có bản cập nhật mới không
  static Future<UpdateInfo?> checkForUpdate() async {
    try {
      final response = await http.get(Uri.parse(updateDocUrl));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final updateInfo = UpdateInfo.fromFirestore(data);

        // Lấy version hiện tại (từ pubspec.yaml hoặc config)
        // package_info_plus có thể lấy version từ native build
        final packageInfo = await PackageInfo.fromPlatform();
        String currentVersion = packageInfo.version;
        
        // Nếu bạn custom version trong C++ hoặc chưa set đúng trong pubspec, 
        // có thể hardcode fallback ở đây
        if (currentVersion.isEmpty || currentVersion == '1.0.0') {
          // currentVersion = '26.08.01.a.public'; // Demo default
        }

        if (_isNewerVersion(updateInfo.latestVersion, currentVersion)) {
          return updateInfo;
        }
      }
    } catch (e) {
      print('Lỗi kiểm tra cập nhật: $e');
    }
    return null;
  }

  /// Tải file setup.exe về máy ngầm và cài đặt
  static Future<void> downloadAndInstallUpdate({
    required String downloadUrl,
    Function(double progress)? onProgress,
    Function(String error)? onError,
  }) async {
    try {
      final tempDir = await getTemporaryDirectory();
      final savePath = '${tempDir.path}\\mytv4u_update.exe';

      await _dio.download(
        downloadUrl,
        savePath,
        onReceiveProgress: (received, total) {
          if (total != -1 && onProgress != null) {
            onProgress(received / total);
          }
        },
      );

      // Chạy file setup.exe với cờ cài đặt ngầm
      await Process.start(
        savePath,
        ['/VERYSILENT', '/SUPPRESSMSGBOXES', '/CLOSEAPPLICATIONS'],
        mode: ProcessStartMode.detached,
      );

      // Tắt ứng dụng hiện tại để Inno Setup cài đè
      exit(0);
    } catch (e) {
      print('Lỗi tải/cài đặt cập nhật: $e');
      if (onError != null) {
        onError(e.toString());
      }
    }
  }

  /// So sánh chuỗi phiên bản: "26.08.08.a.public"
  static bool _isNewerVersion(String latest, String current) {
    if (latest == current) return false;
    // Tạm thời so sánh chuỗi đơn giản (String compare).
    // Do cấu trúc năm.tháng.ngày nên so sánh chuỗi hoạt động khá tốt
    // VD: "26.08.08.a" > "26.08.07.b"
    return latest.compareTo(current) > 0;
  }
}
