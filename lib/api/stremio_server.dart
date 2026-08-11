import 'dart:async';
import 'dart:io';

/// Manages the Stremio streaming server process (stremio-runtime.exe + server.cjs).
/// This provides a local HTTP server at 127.0.0.1:11470 that can stream
/// torrent content via infoHash URLs.
class StremioServer {
  static Process? _process;
  static bool _isStarting = false;
  static const int port = 11470;
  static const String baseUrl = 'http://127.0.0.1:$port';

  /// Whether the server process is currently running.
  static bool get isRunning => _process != null;

  /// Get the path to the stremio_server directory relative to the app executable.
  static String get _serverDir {
    final exeDir = File(Platform.resolvedExecutable).parent.path;
    return '$exeDir${Platform.pathSeparator}stremio_server';
  }

  /// Start the Stremio streaming server in the background.
  /// Returns true if server started successfully, false otherwise.
  static Future<bool> start() async {
    if (_isStarting || isRunning) return isRunning;
    _isStarting = true;

    try {
      final serverDir = _serverDir;
      final runtimeExe = '$serverDir${Platform.pathSeparator}stremio-runtime.exe';
      final serverScript = 'server.cjs';

      // Check if required files exist
      if (!File(runtimeExe).existsSync()) {
        print('StremioServer: stremio-runtime.exe not found at $runtimeExe');
        _isStarting = false;
        return false;
      }
      if (!File('$serverDir${Platform.pathSeparator}$serverScript').existsSync()) {
        print('StremioServer: server.cjs not found');
        _isStarting = false;
        return false;
      }

      // Kill any existing stremio-runtime process on this port
      await _killExisting();

      // [Dynamic RAM Rule] DO NOT REMOVE
      // Dynamically allocate Node.js RAM limit based on system RAM
      int totalRamMb = await _getSystemMemoryMB();
      int nodeRamLimit = 128; // <= 4GB
      
      if (totalRamMb > 16384) {
        nodeRamLimit = 2048; // > 16GB (e.g. 32GB) -> 2GB
      } else if (totalRamMb > 8192) {
        nodeRamLimit = 1024; // > 8GB (e.g. 16GB) -> 1GB
      } else if (totalRamMb > 4096) {
        nodeRamLimit = 256; // > 4GB (e.g. 8GB) -> 256MB
      }
      
      // Start the server process
      print('StremioServer: Starting server from $serverDir with ${nodeRamLimit}MB RAM (System RAM: ${totalRamMb}MB)');
      _process = await Process.start(
        runtimeExe,
        [serverScript],
        workingDirectory: serverDir,
        mode: ProcessStartMode.normal,
        environment: {
          'NODE_OPTIONS': '--max-old-space-size=$nodeRamLimit', // Dynamic allocation
        },
      );
      
      // Drain stdout and stderr to prevent the Node process from blocking
      _process!.stdout.listen((_) {});
      _process!.stderr.listen((_) {});

      print('StremioServer: Process started with PID ${_process!.pid}');

      // Wait for the server to be ready (up to 10 seconds)
      final ready = await _waitForReady(timeout: const Duration(seconds: 10));
      if (ready) {
        print('StremioServer: Server is ready at $baseUrl');
      } else {
        print('StremioServer: Server started but not responding yet (may still be initializing)');
      }

      _isStarting = false;
      return true;
    } catch (e) {
      print('StremioServer: Failed to start: $e');
      _isStarting = false;
      return false;
    }
  }

  /// Stop the Stremio streaming server.
  static Future<void> stop() async {
    if (_process != null) {
      try {
        print('StremioServer: Stopping server (PID ${_process!.pid})');
        Process.killPid(_process!.pid, ProcessSignal.sigterm);
      } catch (e) {
        print('StremioServer: Error stopping: $e');
      }
      _process = null;
    }
    // Also kill any stray stremio-runtime processes
    await _killExisting();
  }

  /// Build a streaming URL for a given torrent infoHash and file index.
  static String buildStreamUrl(String infoHash, int fileIdx) {
    return '$baseUrl/$infoHash/$fileIdx';
  }

  /// Check if the server is responding.
  static Future<bool> isReady() async {
    try {
      final client = HttpClient();
      client.connectionTimeout = const Duration(seconds: 2);
      final request = await client.getUrl(Uri.parse(baseUrl));
      final response = await request.close().timeout(const Duration(seconds: 3));
      await response.drain();
      client.close();
      return response.statusCode == 200;
    } catch (_) {
      return false;
    }
  }

  /// Wait for the server to become ready.
  static Future<bool> _waitForReady({required Duration timeout}) async {
    final deadline = DateTime.now().add(timeout);
    while (DateTime.now().isBefore(deadline)) {
      if (await isReady()) return true;
      await Future.delayed(const Duration(milliseconds: 500));
    }
    return false;
  }

  /// Kill any existing stremio-runtime processes.
  static Future<void> _killExisting() async {
    try {
      if (Platform.isWindows) {
        await Process.run('taskkill', ['/F', '/IM', 'stremio-runtime.exe'],
            runInShell: true);
      }
    } catch (_) {}
  }

  /// Get total system physical memory in MB
  static Future<int> _getSystemMemoryMB() async {
    try {
      if (Platform.isWindows) {
        final res = await Process.run('wmic', ['computersystem', 'get', 'totalphysicalmemory']);
        final output = res.stdout.toString().replaceAll('\r', '').split('\n');
        if (output.length > 1) {
          final bytes = int.tryParse(output[1].trim()) ?? 0;
          return bytes ~/ (1024 * 1024);
        }
      }
    } catch (_) {}
    return 8192; // Default to 8GB if failed
  }
}
