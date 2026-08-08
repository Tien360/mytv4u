import re
import os

path = r't:\Project\Phim\mytv4u_flutter\lib\screens\movie_detail_screen.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace everything from "if (_premiumServers.isNotEmpty) ...["
# down to "// The episodes grid" and the episodes grid itself, replacing it with the new UI.

# Let's find the start index:
start_str = "                              if (_premiumServers.isNotEmpty) ...["
end_str = "                              _buildCommentsSection(),"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx == -1 or end_idx == -1:
    print("Could not find start or end markers")
    exit(1)

new_ui = """
                              // --- TABS CHÍNH ---
                              Row(
                                children: [
                                  _buildMainTab('Promax', 'NGUỒN PROMAX', Icons.stars),
                                  const SizedBox(width: 16),
                                  _buildMainTab('Standard', 'NGUỒN STANDARD', Icons.list),
                                ],
                              ),
                              const SizedBox(height: 24),
                              
                              // --- NỘI DUNG THEO TAB CHÍNH ---
                              if (_activeMainTab == 'Promax') ...[
                                // Hiển thị các nút chọn nguồn Promax (Premium, P2P)
                                Builder(builder: (context) {
                                  final promaxServers = [..._premiumServers, ..._p2pServers];
                                  if (promaxServers.isEmpty) return const Text('Không có nguồn Promax nào.', style: TextStyle(color: Colors.white54));
                                  return Wrap(
                                    spacing: 12, runSpacing: 12,
                                    children: promaxServers.map((s) => _buildServerTab(s, isPremium: s.serverName.toLowerCase().contains('premium'))).toList(),
                                  );
                                }),
                              ] else if (_activeMainTab == 'Standard') ...[
                                // Sub-tabs: Thuyết minh / Phụ đề
                                Row(
                                  children: [
                                    _buildSubTab('Vietsub', 'Phụ đề'),
                                    const SizedBox(width: 12),
                                    _buildSubTab('Thuyết Minh', 'Thuyết minh / Lồng tiếng'),
                                  ],
                                ),
                                const SizedBox(height: 16),
                                
                                // Hiển thị các nguồn Standard dựa theo Sub-tab
                                Builder(builder: (context) {
                                  final targetServers = _activeStandardSubTab == 'Vietsub' ? _vietsubServers : _tmServers;
                                  if (targetServers.isEmpty) return const Text('Không có nguồn nào trong mục này.', style: TextStyle(color: Colors.white54));
                                  
                                  final List<EpisodeServer> displayServers = [];
                                  final motchillGroup = targetServers.where((s) => s.serverName.toLowerCase().startsWith('motchill')).toList();
                                  for (var s in targetServers) {
                                    if (s.serverName.toLowerCase().startsWith('motchill')) {
                                      if (!displayServers.any((x) => x.serverName == 'Motchill Server')) {
                                        displayServers.add(EpisodeServer(serverName: 'Motchill Server', items: [])); // Dummy
                                      }
                                    } else {
                                      displayServers.add(s);
                                    }
                                  }
                                  
                                  return Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Wrap(
                                        spacing: 12, runSpacing: 12,
                                        children: displayServers.map((s) {
                                          if (s.serverName == 'Motchill Server') {
                                            return _buildServerTab(s, isPremium: false, isMotchillGroup: true, motchillGroup: motchillGroup);
                                          }
                                          return _buildServerTab(s, isPremium: false);
                                        }).toList(),
                                      ),
                                      if (_currentServer != null && _currentServer!.serverName.toLowerCase().startsWith('motchill') && motchillGroup.isNotEmpty) ...[
                                        const SizedBox(height: 12),
                                        Container(
                                          padding: const EdgeInsets.only(left: 16),
                                          decoration: BoxDecoration(
                                            border: Border(left: BorderSide(color: Colors.white.withOpacity(0.1), width: 2)),
                                          ),
                                          child: Wrap(
                                            spacing: 8, runSpacing: 8,
                                            children: motchillGroup.map((s) => _buildServerTab(s, isPremium: false, isSubServer: true)).toList(),
                                          ),
                                        ),
                                      ],
                                    ],
                                  );
                                }),
                              ],
                              
                              const SizedBox(height: 32),
                              
                              // --- DANH SÁCH TẬP PHIM / LUỒNG PHÁT ---
                              if (_currentServer != null) ...[
                                Container(
                                  padding: const EdgeInsets.all(24),
                                  decoration: BoxDecoration(
                                    color: Colors.white.withOpacity(0.03),
                                    borderRadius: BorderRadius.circular(16),
                                    border: Border.all(color: Colors.white.withOpacity(0.05)),
                                  ),
                                  child: _buildEpisodesGrid(),
                                ),
                              ],
                              const SizedBox(height: 32),
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(content[:start_idx] + new_ui + content[end_idx:])

print("Successfully replaced UI chunk.")
