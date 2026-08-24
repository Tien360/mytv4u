class AnimatedLogoWidget extends StatefulWidget {
  final dynamic logoPath;
  const AnimatedLogoWidget({Key? key, required this.logoPath}) : super(key: key);

  @override
  State<AnimatedLogoWidget> createState() => _AnimatedLogoWidgetState();
}

class _AnimatedLogoWidgetState extends State<AnimatedLogoWidget> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;
  late int _animationType;
  bool _isHovered = false;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
    _animation = CurvedAnimation(parent: _controller, curve: Curves.easeOutBack);
    
    // Pick a random animation type
    _animationType = DateTime.now().millisecondsSinceEpoch % 4;
    
    Future.delayed(Duration(milliseconds: 300 + (DateTime.now().millisecondsSinceEpoch % 300)), () {
      if (mounted) _controller.forward();
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    Widget child = Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(4),
        boxShadow: _isHovered 
            ? [BoxShadow(color: Colors.white.withValues(alpha: 0.5), blurRadius: 10, spreadRadius: 2)]
            : null,
      ),
      child: Image.network(
        'https://image.tmdb.org/t/p/w200${widget.logoPath}',
        height: 24,
        fit: BoxFit.contain,
      ),
    );

    child = MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      cursor: SystemMouseCursors.click,
      child: AnimatedScale(
        scale: _isHovered ? 1.1 : 1.0,
        duration: const Duration(milliseconds: 200),
        child: child,
      ),
    );

    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        if (_animationType == 0) {
          // Slide up and fade
          return Opacity(
            opacity: _animation.value.clamp(0.0, 1.0),
            child: Transform.translate(
              offset: Offset(0, 20 * (1 - _animation.value)),
              child: child,
            ),
          );
        } else if (_animationType == 1) {
          // Scale up
          return Transform.scale(
            scale: _animation.value,
            child: child,
          );
        } else if (_animationType == 2) {
          // Fade only
          return Opacity(
            opacity: _animation.value.clamp(0.0, 1.0),
            child: child,
          );
        } else {
          // Flip 3D
          import 'dart:math';
          return Transform(
            alignment: Alignment.center,
            transform: Matrix4.identity()
              ..setEntry(3, 2, 0.001)
              ..rotateY(pi * (1 - _animation.value)),
            child: Opacity(
              opacity: _animation.value.clamp(0.0, 1.0),
              child: child,
            ),
          );
        }
      },
      child: child,
    );
  }
}
