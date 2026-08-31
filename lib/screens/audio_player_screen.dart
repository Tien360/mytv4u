import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import '../widgets/tonearm_widget.dart';
import 'package:palette_generator/palette_generator.dart';
import 'package:flutter/services.dart';
import 'audio_visualizer.dart';
import 'package:id3/id3.dart';
import 'dart:convert';
import 'dart:io';

import 'settings_screen.dart';
import '../utils/l10n.dart';
import 'package:media_kit/media_kit.dart';

import 'dart:typed_data';
import 'dart:math' as math;
import 'dart:ui';
import 'package:file_picker/file_picker.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../api/firebase_api.dart';

class AudioPlayerScreen extends StatefulWidget {
  final List<PlatformFile> files;
  final int initialIndex;

  const AudioPlayerScreen({Key? key, required this.files, this.initialIndex = 0}) : super(key: key);

  @override
  _AudioPlayerScreenState createState() => _AudioPlayerScreenState();
}

class _AudioPlayerScreenState extends State<AudioPlayerScreen> with TickerProviderStateMixin {
  late List<PlatformFile> _playlistFiles;
  late final Player player;
  int currentIndex = 0;
  bool isPlaying = false;
  Duration position = Duration.zero;
  Duration duration = Duration.zero;
  Uint8List? coverArt;
  Color _dominantColor = Colors.blueAccent;
  final Map<String, Uint8List?> _coverCache = {};
  String title = '';
  String artist = '';
  bool isShuffle = false;
  int repeatMode = 0; // 0: off, 1: all, 2: one

  late AnimationController _spinController;
  late AnimationController _vizController;
  
  String visualizerType = 'bars';
  int sleepTimerMinutes = 0;
  bool _showPlaylist = false;
  bool showVinyl = true;

  @override
  void initState() {
    super.initState();
    _playlistFiles = List.from(widget.files);
    currentIndex = widget.initialIndex;
    player = Player();
    
    _spinController = AnimationController(vsync: this, duration: const Duration(seconds: 10));
    _vizController = AnimationController(vsync: this, duration: const Duration(milliseconds: 500))..repeat(reverse: true);
    
    _loadSettings();

    player.stream.playing.listen((playing) {
      if (mounted) {
        setState(() => isPlaying = playing);
        if (playing) {
          _spinController.repeat();
          _vizController.repeat(reverse: true);
        } else {
          _spinController.stop();
          _vizController.stop();
        }
      }
    });
    
    player.stream.position.listen((pos) {
      if (mounted) setState(() => position = pos);
    });
    
    player.stream.duration.listen((dur) {
      if (mounted) setState(() => duration = dur);
    });
    
    player.stream.completed.listen((completed) {
      if (completed) {
        _handleCompletion();
      }
    });

    _loadCurrent();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      visualizerType = prefs.getString('audio_visualizer') ?? 'bars';
      sleepTimerMinutes = prefs.getInt('audio_sleep_timer') ?? 0;
      showVinyl = prefs.getBool('audio_vinyl') ?? true;
    });
    
    if (sleepTimerMinutes > 0) {
      Future.delayed(Duration(minutes: sleepTimerMinutes), () {
        if (mounted) player.pause();
      });
    }
  }

  void _handleCompletion() {
    if (repeatMode == 2) {
      player.seek(Duration.zero);
      player.play();
    } else if (isShuffle) {
      currentIndex = math.Random().nextInt(_playlistFiles.length);
      _loadCurrent();
    } else if (currentIndex < _playlistFiles.length - 1) {
      _next();
    } else if (repeatMode == 1) {
      currentIndex = 0;
      _loadCurrent();
    }
  }


  Future<Uint8List?> _getThumbnail(String path) async {
    if (_coverCache.containsKey(path)) return _coverCache[path];
    try {
      if (path.toLowerCase().endsWith('.mp3')) {
        // Read async to avoid freezing UI
        final bytes = await File(path).readAsBytes();
        final mp3 = MP3Instance(bytes);
        if (mp3.parseTagsSync()) {
          final tags = mp3.getMetaTags();
          if (tags != null && tags['APIC'] != null) {
            _coverCache[path] = base64Decode(tags['APIC']['base64']);
            return _coverCache[path];
          }
        }
      }
    } catch (_) {}
    _coverCache[path] = null;
    return null;
  }

  Future<void> _loadCurrent() async {
    final file = _playlistFiles[currentIndex];
    final path = file.path!;
    
    setState(() {
      title = file.name.replaceAll(RegExp(r'\.[a-zA-Z0-9]+$'), '');
      artist = 'Unknown Artist';
      coverArt = null;
    });
    
    // Try to extract ID3 tags
    try {
      if (path.toLowerCase().endsWith('.mp3')) {
        MP3Instance mp3 = MP3Instance(File(path).readAsBytesSync());
        if (mp3.parseTagsSync()) {
          Map<String, dynamic>? tags = mp3.getMetaTags();
          if (tags != null) {
            setState(() {
              title = tags['Title'] ?? title;
              artist = tags['Artist'] ?? artist;
              if (tags['APIC'] != null && tags['APIC']['base64'] != null) {
                coverArt = base64Decode(tags['APIC']['base64']);
              }
            });
          }
        }
      }
    } catch (e) {
      // Ignore id3 parsing errors
    }
    _updateDominantColor();
    
    await player.open(Media(path));
    player.play();
  }

  Future<void> _addFiles(Function setSheetState) async {
    var files = await FilePicker.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['mp3', 'wav', 'flac', 'm4a', 'aac', 'wma', 'ogg'],
      allowMultiple: true,
    );
    if (files != null && files.isNotEmpty) {
      setState(() {
        for (var file in files) {
          if (file.path != null) {
            _playlistFiles.add(file);
          }
        }
      });
      setSheetState(() {});
    }
  }

  Future<void> _updateDominantColor() async {
    if (coverArt == null) {
      if (mounted) setState(() => _dominantColor = Colors.blueAccent);
      return;
    }
    try {
      final PaletteGenerator generator = await PaletteGenerator.fromImageProvider(
        MemoryImage(coverArt!),
        size: const Size(100, 100),
      );
      if (mounted) {
        setState(() {
          _dominantColor = generator.dominantColor?.color ?? generator.vibrantColor?.color ?? Colors.blueAccent;
        });
      }
    } catch (e) {
      if (mounted) setState(() => _dominantColor = Colors.blueAccent);
    }
  }

  void _toggleShuffle() {
    setState(() {
      isShuffle = !isShuffle;
    });
  }

  void _toggleRepeat() {
    setState(() {
      repeatMode = (repeatMode + 1) % 3;
    });
  }

  void _next() {
    if (isShuffle) {
      currentIndex = math.Random().nextInt(_playlistFiles.length);
      _loadCurrent();
    } else if (currentIndex < _playlistFiles.length - 1) {
      currentIndex++;
      _loadCurrent();
    } else if (repeatMode == 1) {
      currentIndex = 0;
      _loadCurrent();
    }
  }

  void _prev() {
    if (position.inSeconds > 3) {
      player.seek(Duration.zero);
    } else if (currentIndex > 0) {
      currentIndex--;
      _loadCurrent();
    } else if (repeatMode == 1) {
      currentIndex = _playlistFiles.length - 1;
      _loadCurrent();
    }
  }

  @override
  void dispose() {
    player.dispose();
    _spinController.dispose();
    _vizController.dispose();
    super.dispose();
  }

  String _formatDuration(Duration d) {
    String twoDigits(int n) => n.toString().padLeft(2, "0");
    String twoDigitMinutes = twoDigits(d.inMinutes.remainder(60));
    String twoDigitSeconds = twoDigits(d.inSeconds.remainder(60));
    if (d.inHours > 0) {
      return "${d.inHours}:$twoDigitMinutes:$twoDigitSeconds";
    }
    return "$twoDigitMinutes:$twoDigitSeconds";
  }



  void _showAudioSettings() {
    showDialog(
      context: context,
      barrierColor: Colors.black.withOpacity(0.5),
      builder: (context) {
        return Center(
          child: Material(
            color: Colors.transparent,
            child: Container(
              width: 500,
              decoration: BoxDecoration(
                color: const Color(0x33000000),
                borderRadius: BorderRadius.circular(24),
                border: Border.all(color: const Color(0x33FFFFFF)),
                boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 20)],
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(24),
                child: BackdropFilter(
                  filter: ui.ImageFilter.blur(sigmaX: 40, sigmaY: 40),
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: StatefulBuilder(
                      builder: (context, setDialogState) {
                        return Column(
                          mainAxisSize: MainAxisSize.min,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(L10n.t('audio_settings') ?? "Cài đặt Trình phát", style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                            const SizedBox(height: 24),
                            ListTile(
                              leading: const Icon(Icons.graphic_eq, color: Colors.white),
                              title: Text(L10n.t('visualizer_type') ?? 'Kiểu sóng âm', style: const TextStyle(color: Colors.white)),
                              trailing: DropdownButton<String>(
                                dropdownColor: Colors.grey[900],
                                value: ['none', 'inline', 'bars', 'circle'].contains(visualizerType) ? visualizerType : 'bars',
                                underline: const SizedBox(),
                                items: [
                                  DropdownMenuItem(value: 'none', child: Text(L10n.t('viz_none') ?? 'Tắt', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'inline', child: Text(L10n.t('viz_inline') ?? 'Nhỏ (cạnh tên)', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'bars', child: Text(L10n.t('viz_bars') ?? 'Lớn (dưới ảnh)', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 'circle', child: Text(L10n.t('viz_circle') ?? 'Vòng tròn đĩa', style: const TextStyle(color: Colors.white))),
                                ],
                                onChanged: (val) async {
                                  if (val != null) {
                                    final prefs = await SharedPreferences.getInstance();
                                    prefs.setString('audio_visualizer', val);
                                    FirebaseApi.saveUserSettings({'audio_visualizer': val});
                                    setDialogState(() => visualizerType = val);
                                    setState(() => visualizerType = val);
                                  }
                                },
                              ),
                            ),
                            ListTile(
                              leading: const Icon(Icons.album, color: Colors.white),
                              title: Text(L10n.t('vinyl_effect') ?? 'Hiệu ứng Đĩa than', style: const TextStyle(color: Colors.white)),
                              trailing: Switch(
                                value: showVinyl,
                                activeColor: Colors.blueAccent,
                                onChanged: (val) async {
                                  final prefs = await SharedPreferences.getInstance();
                                  prefs.setBool('audio_vinyl', val);
                                  FirebaseApi.saveUserSettings({'audio_vinyl': val});
                                  setDialogState(() => showVinyl = val);
                                  setState(() => showVinyl = val);
                                },
                              ),
                            ),
                            ListTile(
                              leading: const Icon(Icons.timer, color: Colors.white),
                              title: Text(L10n.t('sleep_timer') ?? 'Hẹn giờ tắt (phút)', style: const TextStyle(color: Colors.white)),
                              trailing: DropdownButton<int>(
                                dropdownColor: Colors.grey[900],
                                value: sleepTimerMinutes,
                                underline: const SizedBox(),
                                items: [
                                  DropdownMenuItem(value: 0, child: Text(L10n.t('off') ?? 'Tắt', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 15, child: const Text('15', style: TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 30, child: const Text('30', style: TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 60, child: const Text('60', style: TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 120, child: const Text('120', style: TextStyle(color: Colors.white))),
                                ],
                                onChanged: (val) async {
                                  if (val != null) {
                                    final prefs = await SharedPreferences.getInstance();
                                    prefs.setInt('audio_sleep_timer', val);
                                    FirebaseApi.saveUserSettings({'audio_sleep_timer': val});
                                    setDialogState(() => sleepTimerMinutes = val);
                                    setState(() => sleepTimerMinutes = val);
                                    if (val > 0) {
                                      Future.delayed(Duration(minutes: val), () {
                                        if (mounted) player.pause();
                                      });
                                    }
                                  }
                                },
                              ),
                            ),
                            ListTile(
                              leading: const Icon(Icons.repeat, color: Colors.white),
                              title: Text(L10n.t('repeat_mode') ?? 'Chế độ lặp lại', style: const TextStyle(color: Colors.white)),
                              trailing: DropdownButton<int>(
                                dropdownColor: Colors.grey[900],
                                value: repeatMode,
                                underline: const SizedBox(),
                                items: [
                                  DropdownMenuItem(value: 0, child: Text(L10n.t('repeat_none') ?? 'Không lặp', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 1, child: Text(L10n.t('repeat_all') ?? 'Lặp danh sách', style: const TextStyle(color: Colors.white))),
                                  DropdownMenuItem(value: 2, child: Text(L10n.t('repeat_one') ?? 'Lặp 1 bài', style: const TextStyle(color: Colors.white))),
                                ],
                                onChanged: (val) {
                                  if (val != null) {
                                    setDialogState(() => repeatMode = val);
                                    setState(() => repeatMode = val);
                                  }
                                },
                              ),
                            ),
                            ListTile(
                              leading: const Icon(Icons.keyboard, color: Colors.white),
                              title: Text(L10n.t('shortcuts') ?? 'Phím tắt', style: const TextStyle(color: Colors.white)),
                              trailing: const Text('Space, ←/→, M, S, R', style: TextStyle(color: Colors.white54, fontSize: 14)),
                            ),
                            ListTile(
                              leading: const Icon(Icons.info_outline, color: Colors.white),
                              title: Text(L10n.t('audio_quality') ?? 'Chất lượng âm thanh', style: const TextStyle(color: Colors.white)),
                              trailing: Builder(
                                builder: (context) {
                                  String qualityInfo = L10n.t('unknown') ?? "Chưa rõ";
                                  if (duration.inSeconds > 0 && _playlistFiles.isNotEmpty) {
                                    try {
                                      int bytes = File(_playlistFiles[currentIndex].path!).lengthSync();
                                      int kbps = ((bytes * 8) / duration.inSeconds / 1000).round();
                                      qualityInfo = " kbps";
                                      if (kbps > 320) qualityInfo += " (Lossless)";
                                      else if (kbps >= 256) qualityInfo += " (HQ)";
                                      else if (kbps >= 128) qualityInfo += " (Standard)";
                                    } catch (e) {
                                      qualityInfo = L10n.t('error_read_file') ?? "Lỗi đọc file";
                                    }
                                  }
                                  return Text(qualityInfo, style: const TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.bold));
                                }
                              ),
                            ),
                          ],
                        );
                      }
                    ),
                  ),
                ),
              ),
            ),
          ),
        );
      }
    );
  }

  Future<Uint8List?> _getCoverForFile(String path) async {
    if (_coverCache.containsKey(path)) return _coverCache[path];
    try {
      if (path.toLowerCase().endsWith('.mp3')) {
        MP3Instance mp3 = MP3Instance(File(path).readAsBytesSync());
        if (mp3.parseTagsSync()) {
          Map<String, dynamic>? tags = mp3.getMetaTags();
          if (tags != null && tags['APIC'] != null && tags['APIC']['base64'] != null) {
            Uint8List bytes = base64Decode(tags['APIC']['base64']);
            _coverCache[path] = bytes;
            return bytes;
          }
        }
      }
    } catch (e) {
      // Ignore
    }
    return null;
  }

  Widget _buildPlaylistPanel() {
    return AnimatedPositioned(
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
      top: 0, bottom: 0,
      right: _showPlaylist ? 0 : -350,
      width: 350,
      child: Material(
        color: Colors.transparent,
        child: Container(
          decoration: BoxDecoration(
            color: Colors.black.withOpacity(0.85),
            border: const Border(left: BorderSide(color: Colors.white24, width: 1)),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(L10n.t('playlist') ?? "Danh sách phát", style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                  Row(
                    children: [
                      IconButton(
                        icon: const Icon(Icons.add_circle_outline, color: Colors.blueAccent),
                        onPressed: () => _addFiles((fn) => setState(fn as void Function())),
                        tooltip: L10n.t('add_to_playlist') ?? 'Thêm nhạc',
                      ),
                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.white54),
                        onPressed: () => setState(() => _showPlaylist = false),
                      ),
                    ],
                  ),
                ],
              ),
              const Divider(color: Colors.white24, height: 32),
              Expanded(
                child: ListView.builder(
                  itemCount: _playlistFiles.length,
                  itemBuilder: (context, i) {
                    final isCurrent = i == currentIndex;
                    return InkWell(
                      onTap: () {
                        setState(() {
                          currentIndex = i;
                          _loadCurrent();
                        });
                      },
                      child: Container(
                        padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 8),
                        decoration: BoxDecoration(
                          color: isCurrent ? Colors.blueAccent.withOpacity(0.2) : Colors.transparent,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Row(
                          children: [
                            Container(
                              width: 48,
                              height: 48,
                              decoration: BoxDecoration(
                                color: Colors.white10,
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: isCurrent
                                  ? AudioVisualizer(isPlaying: isPlaying, type: 'inline', color: _dominantColor)
                                  : FutureBuilder<Uint8List?>(
                                      future: _getCoverForFile(_playlistFiles[i].path!),
                                      builder: (context, snapshot) {
                                        if (snapshot.hasData && snapshot.data != null) {
                                          return ClipRRect(
                                            borderRadius: BorderRadius.circular(8),
                                            child: Image.memory(snapshot.data!, fit: BoxFit.cover),
                                          );
                                        }
                                        return const Icon(Icons.music_note, color: Colors.white54);
                                      },
                                    ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Text(
                                _playlistFiles[i].name,
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: TextStyle(
                                  color: isCurrent ? Colors.blueAccent : Colors.white,
                                  fontWeight: isCurrent ? FontWeight.bold : FontWeight.normal,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    bool isPodcast = duration.inMinutes >= 30;

    Widget infoWidget = Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text(
          title.isEmpty ? L10n.t('unknown_track') ?? 'Unknown Track' : title,
          style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 8),
        Text(
          artist.isEmpty ? L10n.t('unknown_artist') ?? 'Unknown Artist' : artist,
          style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 18),
          textAlign: TextAlign.center,
        ),
      ],
    );

    Widget controlsWidget = Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        SliderTheme(
          data: SliderThemeData(
            trackHeight: 4,
            thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 6),
            overlayShape: const RoundSliderOverlayShape(overlayRadius: 14),
            activeTrackColor: Colors.white,
            inactiveTrackColor: Colors.white.withOpacity(0.2),
            thumbColor: Colors.white,
            overlayColor: Colors.white.withOpacity(0.1),
          ),
          child: Slider(
            value: position.inMilliseconds.toDouble(),
            max: math.max(duration.inMilliseconds.toDouble(), position.inMilliseconds.toDouble() + 1),
            onChanged: (val) {
              player.seek(Duration(milliseconds: val.toInt()));
            },
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 4.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(_formatDuration(position), style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 12)),
              Text(_formatDuration(duration), style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 12)),
            ],
          ),
        ),
        const SizedBox(height: 16),
        Padding(
          padding: const EdgeInsets.only(bottom: 24.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              IconButton(
                icon: Icon(Icons.shuffle, color: isShuffle ? Colors.blueAccent : Colors.white.withOpacity(0.5)),
                iconSize: 28,
                tooltip: L10n.t('shuffle') ?? 'Trộn bài',
                onPressed: _toggleShuffle,
              ),
              IconButton(
                icon: const Icon(Icons.skip_previous_rounded, color: Colors.white),
                iconSize: 48,
                tooltip: L10n.t('prev') ?? 'Bài trước',
                onPressed: _prev,
              ),
              Container(
                width: 72,
                height: 72,
                decoration: const BoxDecoration(shape: BoxShape.circle, color: Colors.white),
                child: IconButton(
                  icon: Icon(isPlaying ? Icons.pause_rounded : Icons.play_arrow_rounded, color: Colors.black),
                  iconSize: 42,
                  tooltip: L10n.t('play_pause') ?? 'Phát/Tạm dừng',
                  onPressed: () {
                    if (isPlaying) player.pause();
                    else player.play();
                  },
                ),
              ),
              IconButton(
                icon: const Icon(Icons.skip_next_rounded, color: Colors.white),
                iconSize: 48,
                tooltip: L10n.t('next') ?? 'Bài tiếp',
                onPressed: _next,
              ),
              IconButton(
                icon: Icon(
                  repeatMode == 0 ? Icons.repeat : (repeatMode == 1 ? Icons.repeat : Icons.repeat_one),
                  color: repeatMode != 0 ? Colors.blueAccent : Colors.white.withOpacity(0.5)
                ),
                iconSize: 28,
                tooltip: L10n.t('repeat') ?? 'Lặp lại',
                onPressed: _toggleRepeat,
              ),
            ],
          ),
        ),
      ],
    );

    return Focus(
      autofocus: true,
      onKeyEvent: (node, event) {
        if (event is KeyDownEvent) {
          if (event.logicalKey == LogicalKeyboardKey.escape) {
            Navigator.pop(context);
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.space) {
            isPlaying ? player.pause() : player.play();
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.arrowRight) {
            player.seek(position + const Duration(seconds: 10));
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.arrowLeft) {
            player.seek(position - const Duration(seconds: 10));
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.keyN) {
            _next();
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.keyP) {
            _prev();
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.keyM) {
            player.setVolume(player.state.volume > 0 ? 0 : 100);
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.keyS) {
            _toggleShuffle();
            return KeyEventResult.handled;
          }
          if (event.logicalKey == LogicalKeyboardKey.keyR) {
            _toggleRepeat();
            return KeyEventResult.handled;
          }
        }
        return KeyEventResult.ignored;
      },
      child: Listener(
        onPointerDown: (event) {
          if (event.buttons == 2) { // Right click
            _showAudioSettings();
          }
        },
        child: Scaffold(
          backgroundColor: Colors.black,
          body: Stack(
            fit: StackFit.expand,
            children: [
              // Main content layout
              LayoutBuilder(
                builder: (context, constraints) {
                  bool isLandscape = constraints.maxWidth > 700;
                  
                  Widget artworkWidget = Hero(
                    tag: 'artwork',
                    child: AnimatedSwitcher(
                      duration: const Duration(milliseconds: 600),
                      switchInCurve: Curves.easeOut,
                      switchOutCurve: Curves.easeIn,
                      transitionBuilder: (child, animation) {
                        return FadeTransition(
                          opacity: animation,
                          child: SlideTransition(
                            position: Tween<Offset>(begin: const Offset(0.05, 0), end: Offset.zero).animate(animation),
                            child: child,
                          ),
                        );
                      },
                      child: KeyedSubtree(
                        key: ValueKey(currentIndex),
                        child: isPodcast
                            ? AspectRatio(
                                aspectRatio: 1,
                                child: Container(
                                  constraints: const BoxConstraints(maxWidth: 320, maxHeight: 320),
                                  decoration: BoxDecoration(
                                    color: Colors.grey[800],
                                    borderRadius: BorderRadius.circular(24),
                                    boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 30, offset: Offset(0, 15))],
                                    image: coverArt != null
                                        ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                        : null,
                                  ),
                                  child: coverArt == null
                                      ? Padding(
                                          padding: const EdgeInsets.all(48.0),
                                          child: Image.asset('assets/images/podcast_icon.png'),
                                        )
                                      : null,
                                ),
                              )
                            : Center(
                                child: Container(
                                  width: 320,
                                  height: 320,
                                  child: Stack(
                                    clipBehavior: Clip.none,
                                    alignment: Alignment.center,
                                    children: [
                                      if (visualizerType == 'circle')
                                        Positioned.fill(
                                          child: AudioVisualizer(isPlaying: isPlaying, type: 'circle', radius: 170, color: _dominantColor),
                                        ),
                                      AnimatedBuilder(
                                      animation: _spinController,
                                      builder: (_, child) {
                                        return Transform.rotate(
                                          angle: showVinyl ? (_spinController.value * 2 * math.pi) : 0,
                                          child: child,
                                        );
                                      },
                                      child: Container(
                                        width: 320,
                                        height: 320,
                                        decoration: BoxDecoration(
                                          shape: BoxShape.circle,
                                          color: const Color(0xFF111111),
                                          boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 20)],
                                          image: coverArt != null
                                              ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                              : null,
                                        ),
                                        child: Stack(
                                          alignment: Alignment.center,
                                          children: [
                                            if (coverArt == null)
                                              Padding(
                                                padding: const EdgeInsets.all(80.0),
                                                child: Image.asset('assets/images/music_icon.png'),
                                              ),
                                            // Semi-transparent overlay to make grooves visible over bright images
                                            if (coverArt != null)
                                              Container(
                                                decoration: const BoxDecoration(
                                                  shape: BoxShape.circle,
                                                  color: Colors.black12,
                                                ),
                                              ),
                                            // Grooves (vân đĩa) over the image
                                            Container(width: 300, height: 300, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 270, height: 270, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 240, height: 240, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 210, height: 210, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 180, height: 180, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 150, height: 150, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 120, height: 120, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 90, height: 90, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            Container(width: 60, height: 60, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white24, width: 1))),
                                            
                                            // Center hole
                                            Container(
                                              width: 16,
                                              height: 16,
                                              decoration: BoxDecoration(
                                                shape: BoxShape.circle,
                                                color: Colors.grey[850],
                                                border: Border.all(color: Colors.black, width: 2),
                                              ),
                                            ),
                                            Container(
                                              width: 6,
                                              height: 6,
                                              decoration: const BoxDecoration(
                                                shape: BoxShape.circle,
                                                color: Colors.black87,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                    ),
                                    if (showVinyl)
                                      Positioned(
                                        top: -10,
                                        right: 10,
                                        child: TonearmWidget(isPlaying: isPlaying),
                                      ),
                                  ],
                                ),
                              ),
                            ),
                      ),
                    ),
                  );

                  Widget content = isLandscape
                      ? Row(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            Expanded(
                              flex: 5,
                              child: Center(
                                child: Padding(
                                  padding: const EdgeInsets.all(32.0),
                                  child: artworkWidget,
                                ),
                              ),
                            ),
                            Expanded(
                              flex: 5,
                              child: Padding(
                                padding: const EdgeInsets.only(right: 64.0, left: 16.0),
                                child: Column(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    infoWidget,
                                    const SizedBox(height: 48),
                                    controlsWidget,
                                  ],
                                ),
                              ),
                            ),
                          ],
                        )
                      : Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 32.0),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Expanded(
                                child: Center(
                                  child: Padding(
                                    padding: const EdgeInsets.symmetric(vertical: 16.0),
                                    child: artworkWidget,
                                  ),
                                ),
                              ),
                              infoWidget,
                              const SizedBox(height: 24),
                              controlsWidget,
                            ],
                          ),
                        );
                  
                  return Stack(
                    children: [
                      // Gradient background
                      Positioned.fill(
                        child: AnimatedContainer(
                          duration: const Duration(seconds: 1),
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              begin: Alignment.topLeft,
                              end: Alignment.bottomRight,
                              colors: [
                                _dominantColor.withOpacity(0.3),
                                Colors.black,
                              ],
                            ),
                          ),
                        ),
                      ),
                      // Main UI
                      content,
                      
                      // Bottom Visualizer
                      if (visualizerType == 'bars' || visualizerType == 'inline')
                        Positioned(
                          left: 0,
                          right: 0,
                          bottom: 0,
                          height: visualizerType == 'inline' ? 80 : 150,
                          child: Opacity(
                            opacity: visualizerType == 'inline' ? 0.5 : 0.8,
                            child: AudioVisualizer(isPlaying: isPlaying, type: visualizerType, color: _dominantColor),
                          ),
                        ),

                      // Top Bar
                      Positioned(
                        top: 0, left: 0, right: 0,
                        child: Container(
                          padding: const EdgeInsets.only(top: 40, bottom: 20, left: 16, right: 16),
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              colors: [Colors.black.withOpacity(0.8), Colors.transparent],
                            ),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              IconButton(
                                icon: const Icon(Icons.keyboard_arrow_down, color: Colors.white, size: 32),
                                onPressed: () => Navigator.pop(context),
                              ),
                              Row(
                                children: [
                                  IconButton(
                                    icon: const Icon(Icons.settings, color: Colors.white),
                                    tooltip: L10n.t('settings') ?? 'Cài đặt',
                                    onPressed: _showAudioSettings,
                                  ),
                                  IconButton(
                                    icon: const Icon(Icons.queue_music, color: Colors.white),
                                    tooltip: L10n.t('playlist') ?? 'Danh sách phát',
                                    onPressed: () => setState(() => _showPlaylist = !_showPlaylist),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      ),
                      
                      // Side Panel Playlist
                      if (_showPlaylist)
                        Positioned.fill(
                          child: GestureDetector(
                            onTap: () => setState(() => _showPlaylist = false),
                            child: Container(color: Colors.transparent),
                          ),
                        ),
                      _buildPlaylistPanel(),
                    ],
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
