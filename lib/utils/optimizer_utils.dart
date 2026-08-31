import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:async';

class OptimizerResult {
  final int ramMB;
  final String cpuName;
  final String gpuName;
  final bool isBattery;
  final double networkMbps;
  final Size resolution;

  OptimizerResult({
    required this.ramMB,
    required this.cpuName,
    required this.gpuName,
    required this.isBattery,
    required this.networkMbps,
    required this.resolution,
  });

  bool get isLowEnd => ramMB <= 4096 || gpuName.toLowerCase().contains('hd graphics');
  bool get isHighEnd => ramMB >= 14000 && !isLowEnd;
}

class OptimizerUtils {
  static Future<int> getRamMB() async {
    if (!Platform.isWindows) return 8192;
    try {
      final res = await Process.run('wmic', ['OS', 'get', 'TotalVisibleMemorySize', '/Value']);
      final match = RegExp(r'TotalVisibleMemorySize=(\d+)').firstMatch(res.stdout.toString());
      if (match != null) {
        return int.parse(match.group(1)!) ~/ 1024;
      }
    } catch (_) {}
    return 8192; // Default
  }

  static Future<String> getCpuName() async {
    if (!Platform.isWindows) return 'Unknown CPU';
    try {
      final res = await Process.run('wmic', ['cpu', 'get', 'Name', '/Value']);
      final match = RegExp(r'Name=(.+)').firstMatch(res.stdout.toString());
      if (match != null) {
        return match.group(1)!.trim();
      }
    } catch (_) {}
    return 'Unknown CPU';
  }

  static Future<String> getGpuName() async {
    if (!Platform.isWindows) return 'Unknown GPU';
    try {
      final res = await Process.run('wmic', ['path', 'win32_VideoController', 'get', 'name', '/Value']);
      final match = RegExp(r'Name=(.+)').firstMatch(res.stdout.toString());
      if (match != null) {
        return match.group(1)!.trim();
      }
    } catch (_) {}
    return 'Unknown GPU';
  }

  static Future<bool> isOnBattery() async {
    if (!Platform.isWindows) return false;
    try {
      final res = await Process.run('wmic', ['path', 'win32_battery', 'get', 'batterystatus', '/Value']);
      final match = RegExp(r'BatteryStatus=(\d+)').firstMatch(res.stdout.toString());
      if (match != null) {
        // 1 = Discharging, 2 = AC
        return match.group(1) == '1';
      }
    } catch (_) {}
    return false; // Assume plugged in if no battery found (desktop)
  }

  static Future<Size> getScreenResolution() async {
    if (!Platform.isWindows) {
      final view = WidgetsBinding.instance.platformDispatcher.views.first;
      return view.physicalSize;
    }
    try {
      final res = await Process.run('wmic', ['path', 'Win32_VideoController', 'get', 'CurrentHorizontalResolution,CurrentVerticalResolution', '/Value']);
      final out = res.stdout.toString();
      final wMatch = RegExp(r'CurrentHorizontalResolution=(\d+)').firstMatch(out);
      final hMatch = RegExp(r'CurrentVerticalResolution=(\d+)').firstMatch(out);
      if (wMatch != null && hMatch != null) {
        return Size(double.parse(wMatch.group(1)!), double.parse(hMatch.group(1)!));
      }
    } catch (_) {}
    
    // Fallback
    final view = WidgetsBinding.instance.platformDispatcher.views.first;
    return view.physicalSize;
  }

  static Future<double> testNetworkSpeed() async {
    try {
      final stopwatch = Stopwatch()..start();
      // Download 5MB chunk from Cloudflare speed test endpoint for better accuracy
      final response = await http.get(Uri.parse('https://speed.cloudflare.com/__down?bytes=5000000')).timeout(const Duration(seconds: 10));
      stopwatch.stop();
      if (response.statusCode == 200) {
        final bytes = response.bodyBytes.length;
        final seconds = stopwatch.elapsedMilliseconds / 1000.0;
        final mbps = (bytes * 8) / (1000000 * seconds);
        return mbps;
      }
    } catch (_) {}
    return 0.0; // Failed
  }
}
