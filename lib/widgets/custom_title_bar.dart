import 'package:flutter/material.dart';
import 'package:window_manager/window_manager.dart';

class CustomTitleBar extends StatelessWidget {
  const CustomTitleBar({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 32.0,
      decoration: const BoxDecoration(
        color: Colors.transparent, // Completely transparent to blend with background
      ),
      child: Row(
        children: [
          // Left Drag area
          Expanded(
            flex: 1,
            child: GestureDetector(
              behavior: HitTestBehavior.translucent,
              onPanStart: (details) {
                windowManager.startDragging();
              },
              onDoubleTap: () async {
                bool isFullScreen = await windowManager.isFullScreen();
                windowManager.setFullScreen(!isFullScreen);
              },
              child: Padding(
                padding: const EdgeInsets.only(left: 16.0),
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Container(),
                ),
              ),
            ),
          ),
          
          // Center Hole for Search Bar (so clicks pass through to underneath)
          Expanded(
            flex: 3,
            child: IgnorePointer(
              child: Container(),
            ),
          ),
          
          // Right Drag area
          Expanded(
            flex: 1,
            child: GestureDetector(
              behavior: HitTestBehavior.translucent,
              onPanStart: (details) {
                windowManager.startDragging();
              },
              onDoubleTap: () async {
                bool isMaximized = await windowManager.isMaximized();
                if (isMaximized) {
                  windowManager.unmaximize();
                } else {
                  windowManager.maximize();
                }
              },
              child: Container(),
            ),
          ),
          
          // Window Controls
          Row(
            children: [
              _WindowButton(
                icon: Icons.minimize,
                onPressed: () => windowManager.minimize(),
              ),
              _WindowButton(
                icon: Icons.crop_square,
                onPressed: () async {
                  bool isFullScreen = await windowManager.isFullScreen();
                  windowManager.setFullScreen(!isFullScreen);
                },
              ),
              _WindowButton(
                icon: Icons.close,
                onPressed: () => windowManager.close(),
                isClose: true,
              ),
            ],
          )
        ],
      ),
    );
  }
}

class _WindowButton extends StatefulWidget {
  final IconData icon;
  final VoidCallback onPressed;
  final bool isClose;

  const _WindowButton({
    required this.icon,
    required this.onPressed,
    this.isClose = false,
  });

  @override
  State<_WindowButton> createState() => _WindowButtonState();
}

class _WindowButtonState extends State<_WindowButton> {
  bool _isHovering = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovering = true),
      onExit: (_) => setState(() => _isHovering = false),
      child: GestureDetector(
        onTap: widget.onPressed,
        child: Container(
          width: 46,
          height: 32,
          color: _isHovering 
            ? (widget.isClose ? Colors.red : Colors.white.withOpacity(0.1))
            : Colors.transparent,
          child: Icon(
            widget.icon,
            size: 16,
            color: Colors.white.withOpacity(0.7),
          ),
        ),
      ),
    );
  }
}
