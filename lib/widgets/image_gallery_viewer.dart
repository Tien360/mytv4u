import 'dart:ui';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';

class ImageGalleryViewer extends StatefulWidget {
  final List<String> images;
  final int initialIndex;

  const ImageGalleryViewer({
    super.key,
    required this.images,
    this.initialIndex = 0,
  });

  @override
  State<ImageGalleryViewer> createState() => _ImageGalleryViewerState();
}

class _ImageGalleryViewerState extends State<ImageGalleryViewer> {
  late PageController _pageController;
  late ScrollController _thumbnailScrollController;
  late int _currentIndex;

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.initialIndex;
    _pageController = PageController(initialPage: _currentIndex);
    _thumbnailScrollController = ScrollController();
    
    // Cuộn đến vị trí ban đầu sau khi build xong
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _scrollToThumbnail(_currentIndex);
    });
  }

  @override
  void dispose() {
    _pageController.dispose();
    _thumbnailScrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: Stack(
        children: [
          // Background Blur
          Positioned.fill(
            child: GestureDetector(
              onTap: () => Navigator.of(context).pop(),
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
                child: Container(
                  color: Colors.black.withOpacity(0.85),
                ),
              ),
            ),
          ),
          
          // Main Image Carousel
          Center(
            child: ScrollConfiguration(
              behavior: ScrollConfiguration.of(context).copyWith(
                dragDevices: {
                  PointerDeviceKind.touch,
                  PointerDeviceKind.mouse,
                  PointerDeviceKind.trackpad,
                },
              ),
              child: PageView.builder(
                controller: _pageController,
                itemCount: widget.images.length,
                onPageChanged: (index) {
                  setState(() {
                    _currentIndex = index;
                  });
                  _scrollToThumbnail(index);
                },
                itemBuilder: (context, index) {
                  return InteractiveViewer(
                    minScale: 1.0,
                    maxScale: 4.0,
                    child: Center(
                      child: CachedNetworkImage(
                        imageUrl: widget.images[index],
                        fit: BoxFit.contain,
                        placeholder: (context, url) => const Center(
                          child: CircularProgressIndicator(color: Colors.amber),
                        ),
                        errorWidget: (context, url, error) => const Icon(
                          Icons.broken_image,
                          color: Colors.white54,
                          size: 64,
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
          ),
          
          // Navigation Buttons (Prev/Next)
          if (widget.images.length > 1) ...[
            if (_currentIndex > 0)
              Positioned(
                left: 24,
                top: 0,
                bottom: 0,
                child: Center(
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.black45,
                      shape: BoxShape.circle,
                    ),
                    child: IconButton(
                      icon: const Padding(
                        padding: EdgeInsets.only(left: 8.0),
                        child: Icon(Icons.arrow_back_ios, color: Colors.white, size: 28),
                      ),
                      onPressed: () {
                        _pageController.previousPage(
                            duration: const Duration(milliseconds: 300),
                            curve: Curves.easeInOut);
                      },
                    ),
                  ),
                ),
              ),
            if (_currentIndex < widget.images.length - 1)
              Positioned(
                right: 24,
                top: 0,
                bottom: 0,
                child: Center(
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.black45,
                      shape: BoxShape.circle,
                    ),
                    child: IconButton(
                      icon: const Icon(Icons.arrow_forward_ios, color: Colors.white, size: 28),
                      onPressed: () {
                        _pageController.nextPage(
                            duration: const Duration(milliseconds: 300),
                            curve: Curves.easeInOut);
                      },
                    ),
                  ),
                ),
              ),
          ],
          
          // Close Button
          Positioned(
            top: 40,
            right: 24,
            child: Container(
              decoration: BoxDecoration(
                color: Colors.black54,
                shape: BoxShape.circle,
                border: Border.all(color: Colors.white24),
              ),
              child: IconButton(
                icon: const Icon(Icons.close, color: Colors.white, size: 28),
                onPressed: () => Navigator.of(context).pop(),
                tooltip: 'Đóng (ESC)',
              ),
            ),
          ),
          
          // Thumbnails
          if (widget.images.length > 1)
            Positioned(
              bottom: 40,
              left: 0,
              right: 0,
              child: SizedBox(
                height: 80,
                child: Center(
                  child: ScrollConfiguration(
                    behavior: ScrollConfiguration.of(context).copyWith(
                      dragDevices: {
                        PointerDeviceKind.touch,
                        PointerDeviceKind.mouse,
                        PointerDeviceKind.trackpad,
                      },
                    ),
                    child: ListView.separated(
                      controller: _thumbnailScrollController,
                      shrinkWrap: true,
                      scrollDirection: Axis.horizontal,
                      itemCount: widget.images.length,
                    separatorBuilder: (context, index) => const SizedBox(width: 12),
                    itemBuilder: (context, index) {
                      final isSelected = index == _currentIndex;
                      return GestureDetector(
                        onTap: () {
                          _pageController.animateToPage(
                            index,
                            duration: const Duration(milliseconds: 300),
                            curve: Curves.easeInOut,
                          );
                        },
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 200),
                          width: 120,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(
                              color: isSelected ? Colors.amber : Colors.transparent,
                              width: 2,
                            ),
                            boxShadow: isSelected
                                ? [BoxShadow(color: Colors.amber.withOpacity(0.5), blurRadius: 8)]
                                : [],
                          ),
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(6),
                            child: CachedNetworkImage(
                              imageUrl: widget.images[index],
                              fit: BoxFit.cover,
                              placeholder: (context, url) => Container(color: Colors.white10),
                              errorWidget: (context, url, error) => Container(color: Colors.white10),
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                ), // End ScrollConfiguration
              ),
            ),
          ),
            
          // Image Counter
          Positioned(
            top: 48,
            left: 24,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              decoration: BoxDecoration(
                color: Colors.black54,
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: Colors.white24),
              ),
              child: Text(
                '${_currentIndex + 1} / ${widget.images.length}',
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                  letterSpacing: 1.5,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _scrollToThumbnail(int index) {
    if (_thumbnailScrollController.hasClients) {
      final double screenWidth = MediaQuery.of(context).size.width;
      final double itemWidth = 120.0 + 12.0; // width + gap
      final double offset = (index * itemWidth) - (screenWidth / 2) + (120.0 / 2);
      
      _thumbnailScrollController.animateTo(
        offset.clamp(0.0, _thumbnailScrollController.position.maxScrollExtent),
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    }
  }
}
