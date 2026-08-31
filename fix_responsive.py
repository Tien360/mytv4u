import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

old_expanded = '''                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 32.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        // Artwork / Vinyl
                        Expanded(
                          child: Center(
                            child: Hero(
                              tag: 'artwork',
                              child: isPodcast
                                  ? AspectRatio(
                                      aspectRatio: 1,
                                      child: Container(
                                        constraints: const BoxConstraints(maxWidth: 350, maxHeight: 350),
                                        decoration: BoxDecoration(
                                          color: Colors.grey[800],
                                          borderRadius: BorderRadius.circular(24),
                                          boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 30, offset: Offset(0, 15))],
                                        ),
                                        child: Padding(
                                          padding: const EdgeInsets.all(48.0),
                                          child: Image.asset('assets/images/podcast_icon.png', color: Colors.blueAccent),
                                        ),
                                      ),
                                    )
                                  : AnimatedBuilder(
                                      animation: _spinController,
                                      builder: (_, child) {
                                        return Transform.rotate(
                                          angle: _spinController.value * 2 * math.pi,
                                          child: child,
                                        );
                                      },
                                      child: AspectRatio(
                                        aspectRatio: 1,
                                        child: Container(
                                          constraints: const BoxConstraints(maxWidth: 380, maxHeight: 380),
                                          decoration: BoxDecoration(
                                            shape: BoxShape.circle,
                                            color: const Color(0xFF1A1A1A),
                                            image: coverArt != null
                                                ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                                : const DecorationImage(image: AssetImage('assets/images/music_icon.png'), fit: BoxFit.cover),
                                            boxShadow: const [BoxShadow(color: Colors.black87, blurRadius: 50, offset: Offset(0, 25))],
                                            border: Border.all(color: Colors.white24, width: 2),
                                          ),
                                          child: Stack(
                                            alignment: Alignment.center,
                                            children: [
                                              if (coverArt != null)
                                                Container(
                                                  decoration: BoxDecoration(
                                                    shape: BoxShape.circle,
                                                    color: Colors.black.withOpacity(0.2),
                                                  ),
                                                ),
                                              for (double w = 350; w > 50; w -= 18)
                                                Container(
                                                  width: w,
                                                  height: w,
                                                  decoration: BoxDecoration(
                                                    shape: BoxShape.circle,
                                                    border: Border.all(color: Colors.black.withOpacity(0.12), width: 1),
                                                  ),
                                                ),
                                              Container(
                                                decoration: BoxDecoration(
                                                  shape: BoxShape.circle,
                                                  gradient: LinearGradient(
                                                    begin: Alignment.topLeft,
                                                    end: Alignment.bottomRight,
                                                    colors: [
                                                      Colors.white.withOpacity(0.4),
                                                      Colors.transparent,
                                                      Colors.transparent,
                                                      Colors.white.withOpacity(0.1),
                                                    ],
                                                    stops: const [0.0, 0.3, 0.7, 1.0],
                                                  ),
                                                ),
                                              ),
                                              Container(
                                                width: 16,
                                                height: 16,
                                                decoration: BoxDecoration(
                                                  shape: BoxShape.circle,
                                                  color: Colors.black,
                                                  border: Border.all(color: Colors.white54, width: 1),
                                                  boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 4, offset: Offset(0, 2))],
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ),
                                    ),
                            ),
                          ),
                        ),
                        
                        const SizedBox(height: 20),
                        
                        // Text Info
                        Align(
                          alignment: Alignment.centerLeft,
                          child: Text(
                            title,
                            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        const SizedBox(height: 6),
                        Row(
                          children: [
                            Expanded(
                              child: Text(
                                artist,
                                style: TextStyle(fontSize: 16, color: Colors.white.withOpacity(0.7)),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                            AudioVisualizer(isPlaying: isPlaying, type: visualizerType),
                          ],
                        ),
                        
                        const SizedBox(height: 20),
                        
                        // Progress Bar
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
                        
                        // Time labels
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
                        
                        // Controls
                        Padding(
                          padding: const EdgeInsets.only(bottom: 24.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                            children: [
                              IconButton(
                                icon: Icon(Icons.shuffle, color: isShuffle ? Colors.blueAccent : Colors.white.withOpacity(0.5)),
                                iconSize: 28,
                                onPressed: () => setState(() => isShuffle = !isShuffle),
                              ),
                              IconButton(
                                icon: const Icon(Icons.skip_previous_rounded, color: Colors.white),
                                iconSize: 48,
                                onPressed: _prev,
                              ),
                              Container(
                                width: 72,
                                height: 72,
                                decoration: const BoxDecoration(shape: BoxShape.circle, color: Colors.white),
                                child: IconButton(
                                  icon: Icon(isPlaying ? Icons.pause_rounded : Icons.play_arrow_rounded, color: Colors.black),
                                  iconSize: 42,
                                  onPressed: () {
                                    if (isPlaying) {
                                      player.pause();
                                    } else {
                                      player.play();
                                    }
                                  },
                                ),
                              ),
                              IconButton(
                                icon: const Icon(Icons.skip_next_rounded, color: Colors.white),
                                iconSize: 48,
                                onPressed: _next,
                              ),
                              IconButton(
                                icon: Icon(
                                  repeatMode == 0 ? Icons.repeat : (repeatMode == 1 ? Icons.repeat : Icons.repeat_one),
                                  color: repeatMode != 0 ? Colors.blueAccent : Colors.white.withOpacity(0.5)
                                ),
                                iconSize: 28,
                                onPressed: () {
                                  setState(() {
                                    repeatMode = (repeatMode + 1) % 3;
                                  });
                                },
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),'''

new_expanded = '''                Expanded(
                  child: LayoutBuilder(
                    builder: (context, constraints) {
                      bool isLandscape = constraints.maxWidth > 700;
                      
                      Widget artworkWidget = Hero(
                        tag: 'artwork',
                        child: isPodcast
                            ? AspectRatio(
                                aspectRatio: 1,
                                child: Container(
                                  constraints: const BoxConstraints(maxWidth: 400, maxHeight: 400),
                                  decoration: BoxDecoration(
                                    color: Colors.grey[800],
                                    borderRadius: BorderRadius.circular(24),
                                    boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 30, offset: Offset(0, 15))],
                                  ),
                                  child: Padding(
                                    padding: const EdgeInsets.all(48.0),
                                    child: Image.asset('assets/images/podcast_icon.png', color: Colors.blueAccent),
                                  ),
                                ),
                              )
                            : AnimatedBuilder(
                                animation: _spinController,
                                builder: (_, child) {
                                  return Transform.rotate(
                                    angle: _spinController.value * 2 * math.pi,
                                    child: child,
                                  );
                                },
                                child: AspectRatio(
                                  aspectRatio: 1,
                                  child: Container(
                                    constraints: const BoxConstraints(maxWidth: 450, maxHeight: 450),
                                    decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      color: const Color(0xFF1A1A1A),
                                      image: coverArt != null
                                          ? DecorationImage(image: MemoryImage(coverArt!), fit: BoxFit.cover)
                                          : const DecorationImage(image: AssetImage('assets/images/music_icon.png'), fit: BoxFit.cover),
                                      boxShadow: const [BoxShadow(color: Colors.black87, blurRadius: 50, offset: Offset(0, 25))],
                                      border: Border.all(color: Colors.white24, width: 2),
                                    ),
                                    child: Stack(
                                      alignment: Alignment.center,
                                      children: [
                                        if (coverArt != null)
                                          Container(
                                            decoration: BoxDecoration(
                                              shape: BoxShape.circle,
                                              color: Colors.black.withOpacity(0.2),
                                            ),
                                          ),
                                        for (double w = 420; w > 50; w -= 20)
                                          Container(
                                            width: w,
                                            height: w,
                                            decoration: BoxDecoration(
                                              shape: BoxShape.circle,
                                              border: Border.all(color: Colors.black.withOpacity(0.12), width: 1),
                                            ),
                                          ),
                                        Container(
                                          decoration: BoxDecoration(
                                            shape: BoxShape.circle,
                                            gradient: LinearGradient(
                                              begin: Alignment.topLeft,
                                              end: Alignment.bottomRight,
                                              colors: [
                                                Colors.white.withOpacity(0.4),
                                                Colors.transparent,
                                                Colors.transparent,
                                                Colors.white.withOpacity(0.1),
                                              ],
                                              stops: const [0.0, 0.3, 0.7, 1.0],
                                            ),
                                          ),
                                        ),
                                        Container(
                                          width: 16,
                                          height: 16,
                                          decoration: BoxDecoration(
                                            shape: BoxShape.circle,
                                            color: Colors.black,
                                            border: Border.all(color: Colors.white54, width: 1),
                                            boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 4, offset: Offset(0, 2))],
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                      );

                      Widget infoWidget = Column(
                        crossAxisAlignment: isLandscape ? CrossAxisAlignment.start : CrossAxisAlignment.center,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Align(
                            alignment: isLandscape ? Alignment.centerLeft : Alignment.center,
                            child: Text(
                              title,
                              style: TextStyle(fontSize: isLandscape ? 32 : 24, fontWeight: FontWeight.bold, color: Colors.white),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              textAlign: isLandscape ? TextAlign.left : TextAlign.center,
                            ),
                          ),
                          const SizedBox(height: 6),
                          Row(
                            mainAxisAlignment: isLandscape ? MainAxisAlignment.start : MainAxisAlignment.center,
                            children: [
                              Flexible(
                                child: Text(
                                  artist,
                                  style: TextStyle(fontSize: isLandscape ? 20 : 16, color: Colors.white.withOpacity(0.7)),
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                              const SizedBox(width: 16),
                              AudioVisualizer(isPlaying: isPlaying, type: visualizerType),
                            ],
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
                              mainAxisAlignment: isLandscape ? MainAxisAlignment.spaceBetween : MainAxisAlignment.spaceEvenly,
                              children: [
                                IconButton(
                                  icon: Icon(Icons.shuffle, color: isShuffle ? Colors.blueAccent : Colors.white.withOpacity(0.5)),
                                  iconSize: 28,
                                  onPressed: () => setState(() => isShuffle = !isShuffle),
                                ),
                                IconButton(
                                  icon: const Icon(Icons.skip_previous_rounded, color: Colors.white),
                                  iconSize: 48,
                                  onPressed: _prev,
                                ),
                                Container(
                                  width: 72,
                                  height: 72,
                                  decoration: const BoxDecoration(shape: BoxShape.circle, color: Colors.white),
                                  child: IconButton(
                                    icon: Icon(isPlaying ? Icons.pause_rounded : Icons.play_arrow_rounded, color: Colors.black),
                                    iconSize: 42,
                                    onPressed: () {
                                      if (isPlaying) {
                                        player.pause();
                                      } else {
                                        player.play();
                                      }
                                    },
                                  ),
                                ),
                                IconButton(
                                  icon: const Icon(Icons.skip_next_rounded, color: Colors.white),
                                  iconSize: 48,
                                  onPressed: _next,
                                ),
                                IconButton(
                                  icon: Icon(
                                    repeatMode == 0 ? Icons.repeat : (repeatMode == 1 ? Icons.repeat : Icons.repeat_one),
                                    color: repeatMode != 0 ? Colors.blueAccent : Colors.white.withOpacity(0.5)
                                  ),
                                  iconSize: 28,
                                  onPressed: () {
                                    setState(() {
                                      repeatMode = (repeatMode + 1) % 3;
                                    });
                                  },
                                ),
                              ],
                            ),
                          ),
                        ],
                      );

                      if (isLandscape) {
                        return Row(
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
                        );
                      } else {
                        return Padding(
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
                      }
                    },
                  ),
                ),'''

if old_expanded in content:
    content = content.replace(old_expanded, new_expanded)
    open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
    print("Replaced layout successfully")
else:
    print("Not found")
