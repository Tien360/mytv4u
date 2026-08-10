class UpdateInfo {
  final String latestVersion;
  final String downloadUrl;
  final String releaseNotes;
  final bool isForceUpdate;
  final bool isBeta;
  final bool isDowngrade;

  UpdateInfo({
    required this.latestVersion,
    required this.downloadUrl,
    required this.releaseNotes,
    required this.isForceUpdate,
    this.isBeta = false,
    this.isDowngrade = false,
  });

  factory UpdateInfo.fromFirestore(Map<String, dynamic> json, {bool isBeta = false, bool isDowngrade = false}) {
    final fields = json['fields'] as Map<String, dynamic>? ?? {};
    return UpdateInfo(
      latestVersion: fields['latest_version']?['stringValue'] ?? '',
      downloadUrl: fields['download_url']?['stringValue'] ?? '',
      releaseNotes: fields['release_notes']?['stringValue'] ?? '',
      isForceUpdate: fields['is_force_update']?['booleanValue'] ?? false,
      isBeta: isBeta,
      isDowngrade: isDowngrade,
    );
  }
}
