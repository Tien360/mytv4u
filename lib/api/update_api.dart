import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'package:package_info_plus/package_info_plus.dart';
import '../models/update_info.dart';
import 'firebase_api.dart';

class UpdateApi {
  static const String publicUpdateUrl = '${FirebaseApi.baseUrl}/updates/public';
  static const String betaUpdateUrl = '${FirebaseApi.baseUrl}/updates/beta';
  static final Dio _dio = Dio(
    BaseOptions(
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(minutes: 10), // file ~70MB cần thời gian dài
      followRedirects: true,
      maxRedirects: 10,
      headers: {
        'User-Agent': 'MyTV4U-Updater/1.0',
      },
    ),
  );

  // BẠN SẼ ĐỔI SỐ NÀY MỖI KHI RA MẮT BẢN CẬP NHẬT MỚI:
  static const String currentAppVersion = '26.09.01.4';

  /// Kiểm tra có bản cập nhật mới không
  static Future<UpdateInfo?> checkForUpdate() async {
    if (currentAppVersion.contains('.dev')) return null; // Dev builds never ask for updates

    try {
      final publicRes = await http.get(Uri.parse(publicUpdateUrl));
      final betaRes = await http.get(Uri.parse(betaUpdateUrl));
      
      UpdateInfo? publicInfo;
      UpdateInfo? betaInfo;

      if (publicRes.statusCode == 200) {
        publicInfo = UpdateInfo.fromFirestore(json.decode(publicRes.body));
      }
      if (betaRes.statusCode == 200) {
        betaInfo = UpdateInfo.fromFirestore(json.decode(betaRes.body), isBeta: true);
      }

      String currentVersion = currentAppVersion;
      bool isCurrentUserBeta = currentVersion.contains('.beta');

      // 1. Luôn ưu tiên bản Public nếu nó mới hơn bản hiện tại
      if (publicInfo != null && _isNewerVersion(publicInfo.latestVersion, currentVersion)) {
        return publicInfo;
      }
      
      // 2. Nếu Public không có gì mới, kiểm tra Beta
      if (betaInfo != null && _isNewerVersion(betaInfo.latestVersion, currentVersion)) {
        // Chỉ hiện Beta nếu bản Beta lớn hơn bản Public (tức là tính năng thật sự mới)
        if (publicInfo == null || _isNewerVersion(betaInfo.latestVersion, publicInfo.latestVersion)) {
          if (isCurrentUserBeta) {
            // Người dùng đang dùng Beta -> Trả về update Beta, có thể bắt buộc
            return betaInfo;
          } else {
            // Người dùng đang dùng Public -> Trả về update Beta nhưng KHÔNG bắt buộc
            return UpdateInfo(
              latestVersion: betaInfo.latestVersion,
              downloadUrl: betaInfo.downloadUrl,
              releaseNotes: betaInfo.releaseNotes,
              isForceUpdate: false, // Public lên Beta luôn là tuỳ chọn
              isBeta: true,
            );
          }
        }
      }
    } catch (e) {
      print('Lỗi kiểm tra cập nhật: $e');
    }
    return null;
  }

  /// Lấy thông tin bản Public trực tiếp (Dành cho chức năng Hạ cấp của Beta)
  static Future<UpdateInfo?> getPublicUpdateInfo() async {
    try {
      final publicRes = await http.get(Uri.parse(publicUpdateUrl));
      if (publicRes.statusCode == 200) {
        final info = UpdateInfo.fromFirestore(json.decode(publicRes.body));
        return UpdateInfo(
          latestVersion: info.latestVersion,
          downloadUrl: info.downloadUrl,
          releaseNotes: info.releaseNotes,
          isForceUpdate: false,
          isDowngrade: true,
        );
      }
    } catch (e) {}
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
        options: Options(
          followRedirects: true,
          receiveTimeout: const Duration(minutes: 10),
          headers: {
            'User-Agent': 'MyTV4U-Updater/1.0',
            'Accept': 'application/octet-stream',
          },
        ),
        onReceiveProgress: (received, total) {
          if (total != -1 && onProgress != null) {
            onProgress(received / total);
          }
        },
      );

      // Chạy file setup.exe với cờ cài đặt ngầm
      await Process.start(
        savePath,
        ['/SILENT', '/SUPPRESSMSGBOXES', '/CLOSEAPPLICATIONS'],
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
