import re

with open("lib/screens/sport_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Remove webview import
text = text.replace("import 'package:webview_windows/webview_windows.dart';", "")

new_livescore_widget = """class SportLivescoreWidget extends StatefulWidget {
  const SportLivescoreWidget({Key? key}) : super(key: key);

  @override
  State<SportLivescoreWidget> createState() => _SportLivescoreWidgetState();
}

class _SportLivescoreWidgetState extends State<SportLivescoreWidget> with AutomaticKeepAliveClientMixin {
  LivescoreData? _data;
  bool _isLoading = true;
  int _activeLeagueIndex = 0;

  @override
  bool get wantKeepAlive => true;

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  Future<void> _fetchData() async {
    setState(() => _isLoading = true);
    final data = await SportApi.getLiveScores();
    if (mounted) {
      setState(() {
        _data = data;
        _isLoading = false;
        if (_data != null && _activeLeagueIndex >= _data!.leagues.length) {
          _activeLeagueIndex = 0;
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    super.build(context);
    
    if (_isLoading && _data == null) {
      return const Center(child: CircularProgressIndicator());
    }
    
    if (_data == null || _data!.leagues.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.info_outline, color: Colors.white54, size: 48),
            const SizedBox(height: 16),
            const Text('Không có dữ liệu lịch thi đấu.', style: TextStyle(color: Colors.white70)),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _fetchData,
              child: const Text('Thử lại'),
            ),
          ],
        ),
      );
    }
    
    final leagues = _data!.leagues;

    return Column(
      children: [
        // League Tabs
        Container(
          height: 50,
          margin: const EdgeInsets.only(top: 16),
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 24),
            itemCount: leagues.length,
            itemBuilder: (context, index) {
              final isActive = index == _activeLeagueIndex;
              return Padding(
                padding: const EdgeInsets.only(right: 8),
                child: ChoiceChip(
                  label: Text(leagues[index].leagueName),
                  selected: isActive,
                  onSelected: (selected) {
                    if (selected) setState(() => _activeLeagueIndex = index);
                  },
                  selectedColor: Colors.blueAccent,
                  backgroundColor: Colors.white10,
                  labelStyle: TextStyle(
                    color: isActive ? Colors.white : Colors.white70,
                    fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                  ),
                ),
              );
            },
          ),
        ),
        
        // Last update text
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Cập nhật: ${_data!.lastUpdate}',
                style: const TextStyle(color: Colors.white54, fontSize: 12),
              ),
              IconButton(
                icon: const Icon(Icons.refresh, color: Colors.white54, size: 20),
                onPressed: _fetchData,
                padding: EdgeInsets.zero,
                constraints: const BoxConstraints(),
              ),
            ],
          ),
        ),
        
        // Matches List
        Expanded(
          child: RefreshIndicator(
            onRefresh: _fetchData,
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
              itemCount: leagues[_activeLeagueIndex].days.length,
              itemBuilder: (context, dayIndex) {
                final day = leagues[_activeLeagueIndex].days[dayIndex];
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Day Header
                    Container(
                      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                      margin: const EdgeInsets.only(top: 16, bottom: 8),
                      decoration: BoxDecoration(
                        color: Colors.white10,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.calendar_today, color: Colors.blueAccent, size: 16),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              day.date,
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: 14,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    
                    // Matches
                    ...day.matches.map((match) {
                      bool isFinished = match.status == 'FT' || match.status == 'Finished' || match.status == 'played';
                      String displayScore = match.score.isNotEmpty ? match.score : (isFinished ? '?' : 'vs');
                      
                      return Container(
                        margin: const EdgeInsets.only(bottom: 8),
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.black26,
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.white10),
                        ),
                        child: Row(
                          children: [
                            // Time
                            SizedBox(
                              width: 80,
                              child: Text(
                                match.time.replaceAll('<br>', ' '),
                                style: TextStyle(
                                  color: isFinished ? Colors.white54 : Colors.blueAccent,
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                            
                            // Teams & Score
                            Expanded(
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Expanded(
                                    child: Text(
                                      match.teamHome,
                                      textAlign: TextAlign.right,
                                      style: TextStyle(
                                        color: Colors.white,
                                        fontWeight: isFinished ? FontWeight.normal : FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                                    margin: const EdgeInsets.symmetric(horizontal: 12),
                                    decoration: BoxDecoration(
                                      color: isFinished ? Colors.white10 : Colors.redAccent.withValues(alpha: 0.8),
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text(
                                      displayScore,
                                      style: const TextStyle(
                                        color: Colors.white,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                  Expanded(
                                    child: Text(
                                      match.teamAway,
                                      textAlign: TextAlign.left,
                                      style: TextStyle(
                                        color: Colors.white,
                                        fontWeight: isFinished ? FontWeight.normal : FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      );
                    }).toList(),
                  ],
                );
              },
            ),
          ),
        ),
      ],
    );
  }
}
"""

text = re.sub(r'class SportLivescoreWidget extends StatefulWidget \{.*$', new_livescore_widget, text, flags=re.DOTALL)

with open("lib/screens/sport_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated SportLivescoreWidget to use native UI")
