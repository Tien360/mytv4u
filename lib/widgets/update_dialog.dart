import 'dart:io';
import 'package:flutter/material.dart';
import 'glass_container.dart';

import '../models/update_info.dart';
import '../api/update_api.dart';

import '../utils/l10n.dart';

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
      onWillPop: () async =>
          !widget.updateInfo.isForceUpdate && !_isDownloading,
      child: Dialog(
        backgroundColor: Colors.transparent,
        elevation: 0,
        child: GlassContainer(
          width: 450,
          padding: const EdgeInsets.all(24),
          borderRadius: 24,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                widget.updateInfo.isDowngrade
                    ? L10n.t('return_public_version', {
                        'version': widget.updateInfo.latestVersion,
                      })
                    : widget.updateInfo.isBeta
                    ? L10n.t('beta_version', {
                        'version': widget.updateInfo.latestVersion,
                      })
                    : L10n.t('update_new_version', {
                        'version': widget.updateInfo.latestVersion,
                      }),
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),
              if (_error.isNotEmpty) ...[
                Text(
                  L10n.t('update_error', {'error': _error}),
                  style: const TextStyle(color: Colors.redAccent),
                ),
                const SizedBox(height: 16),
              ],
              if (widget.updateInfo.isBeta &&
                  !widget.updateInfo.isDowngrade) ...[
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.redAccent.withValues(alpha: 0.1),
                    border: Border.all(
                      color: Colors.redAccent.withValues(alpha: 0.5),
                    ),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      const Icon(
                        Icons.warning_amber_rounded,
                        color: Colors.redAccent,
                        size: 24,
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          L10n.t('beta_warning'),
                          style: const TextStyle(
                            color: Colors.redAccent,
                            fontSize: 13,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
              ],
              if (!_isDownloading) ...[
                Text(
                  L10n.t('update_details'),
                  style: const TextStyle(
                    color: Colors.amber,
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  widget.updateInfo.releaseNotes,
                  style: const TextStyle(color: Colors.white70, fontSize: 14),
                ),
              ] else ...[
                Text(
                  L10n.t('downloading_update'),
                  style: const TextStyle(color: Colors.white70, fontSize: 16),
                ),
                const SizedBox(height: 16),
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: LinearProgressIndicator(
                    value: _progress,
                    backgroundColor: Colors.white10,
                    color: Colors.amber,
                    minHeight: 8,
                  ),
                ),
                const SizedBox(height: 8),
                Align(
                  alignment: Alignment.centerRight,
                  child: Text(
                    '${(_progress * 100).toStringAsFixed(1)}%',
                    style: const TextStyle(color: Colors.white54, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
              const SizedBox(height: 32),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  if (!_isDownloading && !widget.updateInfo.isForceUpdate)
                    TextButton(
                      onPressed: () => Navigator.of(context).pop(),
                      style: TextButton.styleFrom(
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                      ),
                      child: Text(
                        L10n.t('later'),
                        style: const TextStyle(color: Colors.white54, fontSize: 16),
                      ),
                    ),
                  if (!_isDownloading && widget.updateInfo.isForceUpdate)
                    TextButton(
                      onPressed: () => exit(0),
                      style: TextButton.styleFrom(
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                      ),
                      child: Text(
                        L10n.t('exit_app'),
                        style: const TextStyle(color: Colors.white54, fontSize: 16),
                      ),
                    ),
                  if (!_isDownloading) ...[
                    const SizedBox(width: 12),
                    ElevatedButton(
                      onPressed: _startDownload,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.amber,
                        foregroundColor: Colors.black,
                        padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: Text(
                        widget.updateInfo.isDowngrade
                            ? 'Hạ cấp ngay'
                            : L10n.t('update_now'),
                        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ],
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
