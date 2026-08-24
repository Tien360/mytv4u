class AnimatedMovieLogoWidget extends StatefulWidget {
  final String logoUrl;
  final bool showMainTitle;
  
  const AnimatedMovieLogoWidget({Key? key, required this.logoUrl, required this.showMainTitle}) : super(key: key);

  @override
  State<AnimatedMovieLogoWidget> createState() => _AnimatedMovieLogoWidgetState();
}

class _AnimatedMovieLogoWidgetState extends State<AnimatedMovieLogoWidget> with TickerProviderStateMixin {
  late AnimationController _entryController;
  late AnimationController _sweepController;
  late int _animationType;
  bool _isHovered = false;

  @override
  void initState() {
    super.initState();
    _entryController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    );
    
    _sweepController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2000),
    );

    // 0: Slide from left & Fade
    // 1: Zoom in with bounce
    // 2: Flip 3D (X-axis drop)
    // 3: Elastic slide up
    // 4: Blur & Scale (simulated via scale + fade)
    _animationType = DateTime.now().millisecondsSinceEpoch % 5;

    Future.delayed(const Duration(milliseconds: 200), () {
      if (mounted) _entryController.forward();
    });

    // Start sweep effect periodically
    _startSweepLoop();
  }
  
  void _startSweepLoop() async {
    while (mounted) {
      await Future.delayed(Duration(seconds: 4 + (DateTime.now().millisecondsSinceEpoch % 4)));
      if (mounted) {
        _sweepController.forward(from: 0.0);
      }
    }
  }

  @override
  void dispose() {
    _entryController.dispose();
    _sweepController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    Widget child = Stack(
      alignment: Alignment.centerLeft,
      children: [
        ImageFiltered(
          imageFilter: ImageFilter.blur(sigmaX: 3.0, sigmaY: 3.0),
          child: Image.network(
            widget.logoUrl,
            fit: BoxFit.contain,
            alignment: Alignment.centerLeft,
            color: Colors.white.withValues(alpha: 0.7),
            errorBuilder: (context, error, stackTrace) => const SizedBox(),
          ),
        ),
        Transform.translate(
          offset: const Offset(2, 3),
          child: Image.network(
            widget.logoUrl,
            fit: BoxFit.contain,
            alignment: Alignment.centerLeft,
            color: Colors.black.withValues(alpha: 0.8),
            errorBuilder: (context, error, stackTrace) => const SizedBox(),
          ),
        ),
        AnimatedBuilder(
          animation: _sweepController,
          builder: (context, child) {
            if (_sweepController.value == 0 || _sweepController.value == 1) {
              return child!;
            }
            return ShaderMask(
              blendMode: BlendMode.srcATop,
              shaderCallback: (bounds) {
                final x = _sweepController.value * 3.0 - 1.0; // from -1 to 2
                return LinearGradient(
                  colors: [
                    Colors.transparent,
                    Colors.white.withValues(alpha: 0.1),
                    Colors.white.withValues(alpha: 0.8),
                    Colors.white.withValues(alpha: 0.1),
                    Colors.transparent,
                  ],
                  stops: const [0.0, 0.4, 0.5, 0.6, 1.0],
                  begin: Alignment(x - 0.5, -1),
                  end: Alignment(x + 0.5, 1),
                ).createShader(bounds);
              },
              child: child,
            );
          },
          child: Image.network(
            widget.logoUrl,
            fit: BoxFit.contain,
            alignment: Alignment.centerLeft,
            errorBuilder: (context, error, stackTrace) => const SizedBox(),
          ),
        ),
      ],
    );

    Widget animatedChild = AnimatedBuilder(
      animation: _entryController,
      builder: (context, child) {
        final val = _entryController.value;
        final curve = Curves.easeOutBack.transform(val);
        
        if (_animationType == 0) {
          // Slide from left & Fade
          final ease = Curves.easeOutQuart.transform(val);
          return Opacity(
            opacity: val.clamp(0.0, 1.0),
            child: Transform.translate(
              offset: Offset(-50 * (1 - ease), 0),
              child: child,
            ),
          );
        } else if (_animationType == 1) {
          // Zoom in with bounce
          return Opacity(
            opacity: (val * 2).clamp(0.0, 1.0),
            child: Transform.scale(
              scale: 0.5 + 0.5 * curve,
              child: child,
            ),
          );
        } else if (_animationType == 2) {
          // Flip 3D (X-axis drop)
          return Transform(
            alignment: Alignment.topCenter,
            transform: Matrix4.identity()
              ..setEntry(3, 2, 0.001)
              ..rotateX(pi / 2 * (1 - curve)),
            child: Opacity(
              opacity: val.clamp(0.0, 1.0),
              child: child,
            ),
          );
        } else if (_animationType == 3) {
          // Elastic slide up
          final elastic = Curves.elasticOut.transform(val);
          return Opacity(
            opacity: (val * 2).clamp(0.0, 1.0),
            child: Transform.translate(
              offset: Offset(0, 40 * (1 - elastic)),
              child: child,
            ),
          );
        } else {
          // Swirl / Rotate in
          return Opacity(
            opacity: val.clamp(0.0, 1.0),
            child: Transform.rotate(
              angle: -0.2 * (1 - curve),
              child: Transform.scale(
                scale: 0.8 + 0.2 * curve,
                child: child,
              ),
            ),
          );
        }
      },
      child: child,
    );

    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      cursor: SystemMouseCursors.click,
      child: AnimatedScale(
        scale: _isHovered ? 1.05 : 1.0,
        duration: const Duration(milliseconds: 200),
        child: Container(
          constraints: const BoxConstraints(maxHeight: 120, maxWidth: 500),
          alignment: Alignment.centerLeft,
          margin: EdgeInsets.only(bottom: widget.showMainTitle ? 12 : 8),
          child: animatedChild,
        ),
      ),
    );
  }
}
