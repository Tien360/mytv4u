import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/addon.dart';

class AddonManager {
  static const String _prefKey = 'installed_addons';
  
  // List of currently installed addons
  static List<AddonManifest> installedAddons = [];

  /// Initializes the AddonManager by loading installed addons from SharedPreferences.
  static Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final String? data = prefs.getString(_prefKey);
    if (data != null && data.isNotEmpty) {
      try {
        final List<dynamic> decoded = json.decode(data);
        installedAddons = decoded.map((e) {
          // Backward compatibility if transportUrl was not saved
          String url = e['transportUrl'] ?? '';
          return AddonManifest.fromJson(e as Map<String, dynamic>, url);
        }).toList();
      } catch (e) {
        print('Error loading addons: $e');
        installedAddons = [];
      }
    }
  }

  /// Installs an addon from a manifest URL.
  static Future<bool> installAddon(String url) async {
    try {
      if (!url.startsWith('http')) {
        url = 'https://$url';
      }
      if (!url.endsWith('/manifest.json')) {
        if (!url.endsWith('/')) url += '/';
        url += 'manifest.json';
      }

      final res = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 10));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final manifest = AddonManifest.fromJson(data, url);

        // Check if already installed
        final existingIndex = installedAddons.indexWhere((a) => a.id == manifest.id);
        if (existingIndex >= 0) {
          installedAddons[existingIndex] = manifest; // Update existing
        } else {
          installedAddons.add(manifest);
        }

        await _saveAddons();
        return true;
      }
    } catch (e) {
      print('Error installing addon $url: $e');
    }
    return false;
  }

  /// Uninstalls an addon by its ID.
  static Future<void> uninstallAddon(String id) async {
    installedAddons.removeWhere((a) => a.id == id);
    await _saveAddons();
  }

  /// Saves the current list of installed addons to SharedPreferences.
  static Future<void> _saveAddons() async {
    final prefs = await SharedPreferences.getInstance();
    final List<Map<String, dynamic>> data = installedAddons.map((a) => a.toJson()).toList();
    await prefs.setString(_prefKey, json.encode(data));
  }
}
