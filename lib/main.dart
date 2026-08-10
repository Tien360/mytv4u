import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:media_kit/media_kit.dart';
import 'package:provider/provider.dart';
import 'screens/main_screen.dart';
import 'screens/splash_screen.dart';
import 'widgets/custom_title_bar.dart';
import 'package:window_manager/window_manager.dart';
import 'services/deep_link_service.dart';

import 'package:webview_windows/webview_windows.dart';
import 'api/stremio_server.dart';
import 'utils/l10n.dart';
import 'utils/system_utils.dart';

void main(List<String> args) async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Khởi tạo đa ngôn ngữ
  await L10n.load();

  // Tắt Hardware Acceleration của WebView2 để tránh lỗi màn hình đen trên máy lỗi GPU
  try {
    await WebviewController.initializeEnvironment(
      additionalArguments: '--autoplay-policy=no-user-gesture-required'
    );
  } catch (e) {
    debugPrint('Webview init env error: $e');
  }

  MediaKit.ensureInitialized();
  
  // Lấy thông tin RAM bất đồng bộ để set Buffer video
  SystemUtils.initAsync();
  
  // Initialize deep link service (register protocol + parse args)
  await DeepLinkService.instance.initialize(args);
  
  await windowManager.ensureInitialized();
  
  WindowOptions windowOptions = const WindowOptions(
    size: Size(1280, 720),
    center: true,
    backgroundColor: Colors.transparent,
    skipTaskbar: false,
    titleBarStyle: TitleBarStyle.hidden,
  );
  
  windowManager.waitUntilReadyToShow(windowOptions, () async {
    await windowManager.show();
    await windowManager.focus();
  });

  // Start local torrent streaming server
  StremioServer.start();

  runApp(
    MultiProvider(
      providers: [
        Provider(create: (_) => 'MyTV4U'),
      ],
      child: const MyTV4UApp(),
    ),
  );
}

class MyTV4UApp extends StatelessWidget {
  const MyTV4UApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      navigatorKey: DeepLinkService.navigatorKey,
      title: 'MyTV4U',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF111111),
        primaryColor: const Color(0xFF3B82F6),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF3B82F6),
          secondary: Color(0xFF8B5CF6),
        ),
        useMaterial3: true,
      ),
      builder: (context, child) {
        return CallbackShortcuts(
          bindings: {
            const SingleActivator(LogicalKeyboardKey.f11): () async {
              bool isFullScreen = await windowManager.isFullScreen();
              windowManager.setFullScreen(!isFullScreen);
            },
            const SingleActivator(LogicalKeyboardKey.escape): () async {
              bool isFullScreen = await windowManager.isFullScreen();
              if (isFullScreen) {
                windowManager.setFullScreen(false);
              }
            },
          },
          child: Focus(
            autofocus: true,
            child: Scaffold(
              backgroundColor: Colors.black,
              body: child ?? const SizedBox.shrink(),
            ),
          ),
        );
      },
      home: const SplashScreen(),
    );
  }
}
