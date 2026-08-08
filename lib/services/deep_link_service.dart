import 'dart:io';
import 'dart:async';
import 'package:flutter/material.dart';

/// Service that handles:
/// 1. Registering the `mytv4u://` custom URL protocol in Windows Registry
/// 2. Parsing deep link arguments from command line
/// 3. Providing a stream of deep link events for navigation
class DeepLinkService {
  static final DeepLinkService _instance = DeepLinkService._();
  static DeepLinkService get instance => _instance;
  DeepLinkService._();

  /// Global navigator key for deep link navigation
  static final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

  /// Stream controller for deep link events
  final _deepLinkController = StreamController<DeepLinkData>.broadcast();
  Stream<DeepLinkData> get onDeepLink => _deepLinkController.stream;

  /// The initial deep link (from app launch arguments)
  DeepLinkData? initialDeepLink;

  /// Initialize: register protocol + parse launch args
  Future<void> initialize(List<String> args) async {
    await _registerProtocol();
    _parseLaunchArgs(args);
  }

  /// Register `mytv4u://` protocol handler in Windows Registry
  Future<void> _registerProtocol() async {
    if (!Platform.isWindows) return;

    try {
      final exePath = Platform.resolvedExecutable;
      
      // Use cmd /c reg to properly handle quotes in registry values
      await Process.run('cmd', ['/c', 'reg', 'add',
        r'HKCU\Software\Classes\mytv4u',
        '/ve', '/d', 'URL:MyTV4u Protocol', '/f']);

      await Process.run('cmd', ['/c', 'reg', 'add',
        r'HKCU\Software\Classes\mytv4u',
        '/v', 'URL Protocol', '/d', '', '/f']);

      await Process.run('cmd', ['/c', 'reg', 'add',
        r'HKCU\Software\Classes\mytv4u\shell\open\command',
        '/ve', '/d', '"$exePath" "%1"', '/f']);

      debugPrint('[DeepLink] Protocol mytv4u:// registered → $exePath');
    } catch (e) {
      debugPrint('[DeepLink] Failed to register protocol: $e');
    }
  }

  /// Parse command line arguments for a deep link
  void _parseLaunchArgs(List<String> args) {
    for (final arg in args) {
      if (arg.startsWith('mytv4u://')) {
        final data = _parseUri(arg);
        if (data != null) {
          initialDeepLink = data;
          debugPrint('[DeepLink] Launch deep link: ${data.action} slug=${data.slug}');
        }
        break;
      }
    }
  }

  /// Parse a `mytv4u://` URI into structured data
  DeepLinkData? _parseUri(String rawUri) {
    try {
      // mytv4u://movie?slug=abc&source=nguonc
      final uri = Uri.parse(rawUri);
      final action = uri.host.isNotEmpty ? uri.host : uri.pathSegments.firstOrNull ?? '';
      final slug = uri.queryParameters['slug'] ?? '';
      final source = uri.queryParameters['source'] ?? 'nguonc';

      if (slug.isNotEmpty) {
        return DeepLinkData(action: action, slug: slug, source: source);
      }
    } catch (e) {
      debugPrint('[DeepLink] Parse error: $e');
    }
    return null;
  }

  /// Consume the initial deep link (returns it once then clears it)
  DeepLinkData? consumeInitialDeepLink() {
    final link = initialDeepLink;
    initialDeepLink = null;
    return link;
  }

  void dispose() {
    _deepLinkController.close();
  }
}

/// Data class for a parsed deep link
class DeepLinkData {
  final String action; // e.g. "movie"
  final String slug;
  final String source;

  DeepLinkData({
    required this.action,
    required this.slug,
    this.source = 'nguonc',
  });

  @override
  String toString() => 'DeepLink(action=$action, slug=$slug, source=$source)';
}
