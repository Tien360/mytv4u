import 'dart:io';
import 'package:flutter/material.dart';
import '../models/update_info.dart';
import '../api/update_api.dart';

class UpdateDialog extends StatefulWidget {
  final UpdateInfo updateInfo;

  const UpdateDialog({super.key, required this.updateInfo});

  @override
  State<UpdateDialog> createState() => _UpdateDialogState();
}

class _UpdateDialogState extends State<UpdateDialog> {
  bool _isDownloading = false;
  double _progress = 0.0;
  String _error = '';

  Future<void> _startDownload() async {
    setState(() {
      _isDownloading = true;
      _error = '';
    });

    await UpdateApi.downloadAndInstallUpdate(
      downloadUrl: widget.updateInfo.downloadUrl,
      onProgress: (progress) {
        setState(() {
          _progress = progress;
        });
      },
      onError: (error) {
        setState(() {
          _isDownloading = false;
          _error = error;
        });
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async => !widget.updateInfo.isForceUpdate && !_isDownloading,
      child: AlertDialog(
        backgroundColor: const Color(0xFF1A1A2E),
        title: Text(
          widget.updateInfo.isDowngrade
              ? 'Trở về phiên bản Public (${widget.updateInfo.latestVersion})'
              : widget.updateInfo.isBeta
                  ? 'Phiên bản thử nghiệm Beta (${widget.updateInfo.latestVersion})'
                  : 'Cập nhật phiên bản mới (${widget.updateInfo.latestVersion})',
          style: const TextStyle(color: Colors.white, fontSize: 20),
        ),
        content: SizedBox(
          width: 400,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (_error.isNotEmpty) ...[
                Text(
                  'Lỗi: $_error',
                  style: const TextStyle(color: Colors.redAccent),
                ),
                const SizedBox(height: 16),
              ],
              if (widget.updateInfo.isBeta && !widget.updateInfo.isDowngrade) ...[
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.redAccent.withOpacity(0.1),
                    border: Border.all(color: Colors.redAccent.withOpacity(0.5)),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Row(
                    children: [
                      Icon(Icons.warning_amber_rounded, color: Colors.redAccent, size: 24),
                      SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          'Cảnh báo: Đây là phiên bản thử nghiệm (Beta). Có thể chứa một số lỗi. Hãy sao lưu cấu hình trước khi cài.',
                          style: TextStyle(color: Colors.redAccent, fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
              ],
              if (!_isDownloading) ...[
                const Text(
                  'Chi tiết bản cập nhật:',
                  style: TextStyle(color: Colors.amber, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Text(
                  widget.updateInfo.releaseNotes,
                  style: const TextStyle(color: Colors.white70),
                ),
              ] else ...[
                const Text(
                  'Đang tải xuống bản cập nhật...',
                  style: TextStyle(color: Colors.white70),
                ),
                const SizedBox(height: 16),
                LinearProgressIndicator(
                  value: _progress,
                  backgroundColor: Colors.white10,
                  color: Colors.amber,
                  minHeight: 8,
                ),
                const SizedBox(height: 8),
                Align(
                  alignment: Alignment.centerRight,
                  child: Text(
                    '${(_progress * 100).toStringAsFixed(1)}%',
                    style: const TextStyle(color: Colors.white54),
                  ),
                ),
              ],
            ],
          ),
        ),
        actions: [
          if (!_isDownloading && !widget.updateInfo.isForceUpdate)
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Để sau', style: TextStyle(color: Colors.white54)),
            ),
          if (!_isDownloading && widget.updateInfo.isForceUpdate)
            TextButton(
              onPressed: () => exit(0),
              child: const Text('Thoát ứng dụng', style: TextStyle(color: Colors.white54)),
            ),
          if (!_isDownloading)
            ElevatedButton(
              onPressed: _startDownload,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.amber,
                foregroundColor: Colors.black,
              ),
              child: Text(
                widget.updateInfo.isDowngrade ? 'Hạ cấp ngay' : 'Cập nhật ngay',
              ),
            ),
        ],
      ),
    );
  }
}
