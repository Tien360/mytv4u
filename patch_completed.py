import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update completed listener
old_listen = """        player.stream.completed.listen((completed) {
          if (completed && _autoNext) {
            final isNearEnd =
                !_isLiveStream &&
                _duration.inSeconds > 0 &&
                (_position.inSeconds >= _duration.inSeconds - 120);

            if (isNearEnd) {
              _playNextEpisode();
            } else {"""

new_listen = """        player.stream.completed.listen((completed) {
          if (completed) {
            bool shouldAction = _autoNext || _repeatMode > 0;
            if (!shouldAction) return;
            
            final isNearEnd =
                !_isLiveStream &&
                _duration.inSeconds > 0 &&
                (_position.inSeconds >= _duration.inSeconds - 120);

            if (isNearEnd) {
              _playNextEpisode();
            } else {"""

content = content.replace(old_listen, new_listen)

# 2. Update _playNextEpisode method
old_play_next = """  void _playNextEpisode() {
    if (_repeatMode == 2) {
      _initEpisode(_currentIndex);
    } else if (_currentIndex + 1 < widget.episodes.length) {
      _initEpisode(_currentIndex + 1);
    } else if (_repeatMode == 1 && widget.episodes.isNotEmpty) {
      _initEpisode(0);
    }
  }"""

new_play_next = """  void _playNextEpisode() {
    if (_repeatMode == 2) {
      _initEpisode(_currentIndex);
      return;
    } 
    
    if (_autoNext || _repeatMode == 1) {
      if (_currentIndex + 1 < widget.episodes.length) {
        _initEpisode(_currentIndex + 1);
      } else if (_repeatMode == 1 && widget.episodes.isNotEmpty) {
        _initEpisode(0);
      }
    }
  }"""

content = content.replace(old_play_next, new_play_next)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated completed logic")
