import 'package:flutter/material.dart';
import 'dart:ui';

class UIUtils {
  static void showCustomSnackBar(BuildContext context, String message, {bool isError = false}) {
    ScaffoldMessenger.of(context).clearSnackBars();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: ClipRRect(
          borderRadius: BorderRadius.circular(12),
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
              decoration: BoxDecoration(
                color: isError ? Colors.redAccent.withOpacity(0.8) : const Color(0xFF1E293B).withOpacity(0.8),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.white.withOpacity(0.2)),
              ),
              child: Row(
                children: [
                  Icon(
                    isError ? Icons.error_outline : Icons.check_circle_outline,
                    color: Colors.white,
                    size: 24,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      message, 
                      style: const TextStyle(
                        color: Colors.white, 
                        fontWeight: FontWeight.w500,
                        fontSize: 15
                      )
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        backgroundColor: Colors.transparent,
        behavior: SnackBarBehavior.floating,
        elevation: 0,
        margin: const EdgeInsets.only(bottom: 24, left: 24, right: 24),
        padding: EdgeInsets.zero,
        duration: const Duration(seconds: 3),
      ),
    );
  }
}
