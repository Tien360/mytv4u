import 'dart:ui';
import 'package:flutter/material.dart';
import '../utils/l10n.dart';
import 'home_screen.dart';
import 'explore_screen.dart';
import 'search_screen.dart';
import 'settings_screen.dart';
import 'tv_screen.dart';
import 'library_screen.dart';
import 'sport_screen.dart';
import '../widgets/glass_container.dart';
import '../widgets/custom_title_bar.dart';
import 'package:window_manager/window_manager.dart';
import '../api/stremio_server.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> with WindowListener {
  int _selectedIndex = 0;

  final GlobalKey<ExploreScreenState> _exploreKey = GlobalKey<ExploreScreenState>();
  final GlobalKey<SearchScreenState> _searchKey = GlobalKey<SearchScreenState>();
  final GlobalKey<TvScreenState> _tvKey = GlobalKey<TvScreenState>();
  final GlobalKey<SportScreenState> _sportKey = GlobalKey<SportScreenState>();
  final TextEditingController _searchController = TextEditingController();
  late List<Widget> _screens;
  bool _isSidebarCollapsed = false;

  @override
  void initState() {
    super.initState();
    _screens = [
      HomeScreen(
        key: const PageStorageKey('HomeScreen'),
        onNavigateToExplore: (type, slug) {
          setState(() {
            _selectedIndex = 1;
          });
          _exploreKey.currentState?.setFilter(type, slug);
        },
      ),
      ExploreScreen(key: _exploreKey),
      SearchScreen(key: _searchKey),
      TvScreen(key: _tvKey),
      SportScreen(key: _sportKey),
      const LibraryScreen(key: PageStorageKey('LibraryScreen')),
    ];
    windowManager.addListener(this);
  }

  @override
  void onWindowClose() async {
    await StremioServer.stop();
    await windowManager.destroy();
  }

  @override
  void dispose() {
    windowManager.removeListener(this);
    _searchController.dispose();
    super.dispose();
  }

  Widget _buildNavItem(IconData icon, IconData selectedIcon, String label, int index, {VoidCallback? onTapOverride}) {
    final isSelected = index >= 0 && _selectedIndex == index;
    
    return InkWell(
      borderRadius: BorderRadius.circular(12),
      onTap: onTapOverride ?? () {
        setState(() {
          _selectedIndex = index;
        });
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        margin: const EdgeInsets.symmetric(vertical: 2),
        padding: _isSidebarCollapsed 
            ? const EdgeInsets.all(12)
            : const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          color: isSelected 
              ? const Color(0xFF3B82F6).withOpacity(0.18) 
              : Colors.transparent,
          border: isSelected 
              ? Border.all(color: const Color(0xFF3B82F6).withOpacity(0.5), width: 1.5)
              : null,
          boxShadow: isSelected
              ? [
                  BoxShadow(
                    color: const Color(0xFF3B82F6).withOpacity(0.2),
                    blurRadius: 10,
                    spreadRadius: 1,
                  ),
                ]
              : [],
        ),
        child: Row(
          mainAxisAlignment: _isSidebarCollapsed ? MainAxisAlignment.center : MainAxisAlignment.start,
          children: [
            Icon(
              isSelected ? selectedIcon : icon,
              color: isSelected ? const Color(0xFF3B82F6) : Colors.white70,
              size: 22,
            ),
            if (!_isSidebarCollapsed) ...[
              const SizedBox(width: 14),
              Text(
                label,
                style: TextStyle(
                  color: isSelected ? Colors.white : Colors.white70,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                  fontSize: 15,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Key _stackKey = UniqueKey();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Background Black
          Container(
            color: const Color(0xFF000000),
          ),
          
          // Main Content
          AnimatedPositioned(
            duration: const Duration(milliseconds: 200),
            curve: Curves.easeInOut,
            left: _isSidebarCollapsed ? 80 : 240,
            top: 0,
            right: 0,
            bottom: 0,
            child: Column(
              children: [
                // Spacer for title bar and search bar
                const SizedBox(height: 56),
                Expanded(
                  child: IndexedStack(
                    index: _selectedIndex,
                    children: _screens,
                  ),
                ),
              ],
            ),
          ),

          // Glass Sidebar
          AnimatedPositioned(
            duration: const Duration(milliseconds: 200),
            curve: Curves.easeInOut,
            left: 0,
            top: 0,
            bottom: 0,
            width: _isSidebarCollapsed ? 80 : 240,
            child: GlassContainer(
              borderRadius: 0,
              color: const Color(0x1A000000),
              borderColor: const Color(0x1AFFFFFF),
              blur: 40.0,
              child: Column(
                crossAxisAlignment: _isSidebarCollapsed ? CrossAxisAlignment.center : CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 10),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 24.0),
                    child: Row(
                      mainAxisAlignment: _isSidebarCollapsed ? MainAxisAlignment.center : MainAxisAlignment.spaceBetween,
                      children: [
                        if (!_isSidebarCollapsed)
                          const Row(
                            children: [
                              Icon(Icons.movie_filter, color: Color(0xFF3B82F6), size: 32),
                              SizedBox(width: 12),
                              Text('MyTV4U', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 1.2)),
                            ],
                          ),
                        InkWell(
                          onTap: () => setState(() => _isSidebarCollapsed = !_isSidebarCollapsed),
                          borderRadius: BorderRadius.circular(8),
                          child: const Padding(
                            padding: EdgeInsets.all(4.0),
                            child: Icon(Icons.menu, color: Colors.white70, size: 28),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 16),
                  Padding(
                    padding: EdgeInsets.symmetric(horizontal: _isSidebarCollapsed ? 0 : 12),
                    child: Column(
                      children: [
                        _buildNavItem(Icons.home_outlined, Icons.home, L10n.t('nav_home'), 0),
                        const SizedBox(height: 8),
                        _buildNavItem(Icons.explore_outlined, Icons.explore, L10n.t('nav_explore'), 1),
                        const SizedBox(height: 8),
                        _buildNavItem(Icons.search_outlined, Icons.search, L10n.t('nav_search'), 2),
                        const SizedBox(height: 8),
                        _buildNavItem(Icons.live_tv_outlined, Icons.live_tv, L10n.t('nav_tv'), 3),
                        const SizedBox(height: 8),
                        _buildNavItem(Icons.sports_soccer_outlined, Icons.sports_soccer, L10n.t('nav_sport') ?? 'Thể Thao', 4),
                        const SizedBox(height: 8),
                        _buildNavItem(Icons.favorite_outline, Icons.favorite, L10n.t('nav_favorite'), 5),
                      ],
                    ),
                  ),
                  const Spacer(),
                  Padding(
                    padding: EdgeInsets.all(_isSidebarCollapsed ? 8.0 : 12.0),
                    child: _buildNavItem(Icons.settings_outlined, Icons.settings, L10n.t('nav_settings'), -1, onTapOverride: () async {
                      await Navigator.push(context, MaterialPageRoute(builder: (_) => const SettingsScreen()));
                      setState(() {
                        _stackKey = UniqueKey();
                      });
                    }),
                  ),
                ],
              ),
            ),
          ),
          
          // Custom Title Bar (on top to receive window controls and drag)
          const Positioned(
            top: 0, left: 0, right: 0,
            child: CustomTitleBar(),
          ),

          // Global Search Bar (Moved back to title bar, placed after CustomTitleBar to prioritize clicks)
          AnimatedPositioned(
            duration: const Duration(milliseconds: 200),
            curve: Curves.easeInOut,
            top: 6,
            left: _isSidebarCollapsed ? 80.0 : 240.0,
            right: 0,
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 500),
                child: GlassContainer(
                  height: 40,
                  borderRadius: 20,
                  color: Colors.white.withOpacity(0.1),
                  borderColor: Colors.white.withOpacity(0.2),
                  blur: 30.0,
                  child: Row(
                children: [
                  const SizedBox(width: 16),
                  const Icon(Icons.search, color: Colors.white70, size: 18),
                  const SizedBox(width: 12),
                  Expanded(
                    child: TextField(
                      controller: _searchController,
                      style: const TextStyle(color: Colors.white, fontSize: 14),
                      decoration: InputDecoration(
                        hintText: _selectedIndex == 3 ? 'Tìm kiếm kênh TV...' : _selectedIndex == 4 ? 'Tìm kiếm sự kiện thể thao...' : 'Tìm kiếm phim...',
                        hintStyle: const TextStyle(color: Colors.white38, fontSize: 14),
                        border: InputBorder.none,
                        contentPadding: const EdgeInsets.symmetric(vertical: 9),
                        isDense: true,
                      ),
                      onChanged: (query) {
                        if (_selectedIndex == 3) {
                          _tvKey.currentState?.performSearch(query);
                        } else if (_selectedIndex == 4) {
                          _sportKey.currentState?.performSearch(query);
                        } else {
                          if (_selectedIndex != 2) {
                            setState(() => _selectedIndex = 2);
                          }
                          _searchKey.currentState?.performSearch(query);
                        }
                      },
                      onSubmitted: (value) {
                        if (_selectedIndex == 3) {
                          _tvKey.currentState?.performSearch(value);
                        } else if (_selectedIndex == 4) {
                          _sportKey.currentState?.performSearch(value);
                        } else {
                          if (_selectedIndex != 2) {
                            setState(() => _selectedIndex = 2);
                          }
                          _searchKey.currentState?.performSearch(value);
                        }
                      },
                    ),
                  ),
                  if (_searchController.text.isNotEmpty)
                    IconButton(
                      icon: const Icon(Icons.clear, color: Colors.white54, size: 18),
                      onPressed: () {
                        _searchController.clear();
                        setState(() {});
                        if (_selectedIndex == 3) {
                          _tvKey.currentState?.performSearch('');
                        } else if (_selectedIndex == 4) {
                          _sportKey.currentState?.performSearch('');
                        } else if (_selectedIndex == 2) {
                          _searchKey.currentState?.performSearch('');
                        }
                      },
                    ),
                ],
              ),
            ),
          ),
          ),
          ),
        ],
      ),
    );
  }
}
