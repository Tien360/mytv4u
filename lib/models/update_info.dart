class UpdateInfo {
  final String latestVersion;
  final String downloadUrl;
  final String releaseNotes;
  final bool isForceUpdate;

  UpdateInfo({
    required this.latestVersion,
    required this.downloadUrl,
    required this.releaseNotes,
    required this.isForceUpdate,
  });

  factory UpdateInfo.fromFirestore(Map<String, dynamic> json) {
    final fields = json['fields'] as Map<String, dynamic>? ?? {};
    return UpdateInfo(
      latestVersion: fields['latest_version']?['stringValue'] ?? '',
      downloadUrl: fields['download_url']?['stringValue'] ?? '',
      releaseNotes: fields['release_notes']?['stringValue'] ?? '',
      isForceUpdate: fields['is_force_update']?['booleanValue'] ?? false,
    );
  }
}
