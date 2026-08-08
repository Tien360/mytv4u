import 'package:flutter/material.dart';

class UIUtils {
  static void showCustomSnackBar(BuildContext context, String message, {bool isError = false}) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w500)),
        backgroundColor: isError ? Colors.redAccent.withOpacity(0.9) : const Color(0xFF1E293B).withOpacity(0.9),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        elevation: 0,
        margin: const EdgeInsets.only(bottom: 24, left: 24, right: 24),
        duration: const Duration(seconds: 3),
      ),
    );
  }
}
