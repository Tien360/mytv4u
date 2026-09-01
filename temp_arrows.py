import re

with open("lib/widgets/air_schedule_dialog.dart", "r", encoding="utf-8") as f:
    c = f.read()

# We want to replace the `crewAndGuests` logic inside `build` method of `_ExpandableEpisodeCardState`
# and the rendering block at the bottom, and add the `HorizontalAvatarList` class at the end of the file.

# Find the block where `crewAndGuests` is populated
start_idx = c.find("List<Map<String, dynamic>> crewAndGuests = [];")
end_idx = c.find("return GestureDetector(", start_idx)

new_logic = """
    List<Map<String, dynamic>> crewList = [];
    for (var d in validDirectors) {
      crewList.add({
        'name': d['name'] ?? '',
        'role': L10n.t('director'),
        'profile_path': d['profile_path'] ?? '',
      });
    }
    for (var w in writers) {
      crewList.add({
        'name': w['name'] ?? '',
        'role': L10n.t('writer'),
        'profile_path': w['profile_path'] ?? '',
      });
    }
    
    List<Map<String, dynamic>> guestList = [];
    for (var g in guestStars) {
      guestList.add({
        'name': g['name'] ?? '',
        'role': g['character'] ?? '',
        'profile_path': g['profile_path'] ?? '',
      });
    }
    
    """

c = c[:start_idx] + new_logic + c[end_idx:]

# Now replace the rendering block for Crew & Guests
render_start_idx = c.find("// Crew & Guests")
render_end_idx = c.find("],", c.find("},", c.find("child: ListView.builder(", render_start_idx))) + 2

new_render = """// Crew & Guests
                          if (crewList.isNotEmpty) 
                            HorizontalAvatarList(title: '${L10n.t('director')} & ${L10n.t('writer')}', items: crewList),
                          if (guestList.isNotEmpty)
                            HorizontalAvatarList(title: L10n.t('guest_stars'), items: guestList),
"""

c = c[:render_start_idx] + new_render + c[render_end_idx:]

# Add HorizontalAvatarList class at the end
horizontal_list_code = """
class HorizontalAvatarList extends StatefulWidget {
  final String title;
  final List<Map<String, dynamic>> items;

  const HorizontalAvatarList({super.key, required this.title, required this.items});

  @override
  State<HorizontalAvatarList> createState() => _HorizontalAvatarListState();
}

class _HorizontalAvatarListState extends State<HorizontalAvatarList> {
  final ScrollController _scrollController = ScrollController();
  bool _canScrollLeft = false;
  bool _canScrollRight = false;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_updateScrollButtons);
    WidgetsBinding.instance.addPostFrameCallback((_) => _updateScrollButtons());
  }

  void _updateScrollButtons() {
    if (!_scrollController.hasClients) return;
    setState(() {
      _canScrollLeft = _scrollController.position.pixels > 0;
      _canScrollRight = _scrollController.position.pixels < _scrollController.position.maxScrollExtent;
    });
  }

  void _scrollLeft() {
    _scrollController.animateTo(
      (_scrollController.position.pixels - 300).clamp(0.0, _scrollController.position.maxScrollExtent),
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

  void _scrollRight() {
    _scrollController.animateTo(
      (_scrollController.position.pixels + 300).clamp(0.0, _scrollController.position.maxScrollExtent),
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

  @override
  void dispose() {
    _scrollController.removeListener(_updateScrollButtons);
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.items.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 16),
        Text(
          widget.title,
          style: const TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 12),
        SizedBox(
          height: 140,
          child: Stack(
            children: [
              ListView.builder(
                controller: _scrollController,
                scrollDirection: Axis.horizontal,
                itemCount: widget.items.length,
                itemBuilder: (context, idx) {
                  final person = widget.items[idx];
                  final profilePath = person['profile_path'];
                  final profileUrl = TmdbApi.getImageUrl(profilePath);
                  return Container(
                    width: 90,
                    margin: const EdgeInsets.only(right: 12),
                    child: Column(
                      children: [
                        CircleAvatar(
                          radius: 35,
                          backgroundColor: Colors.white.withValues(alpha: 0.1),
                          backgroundImage: profileUrl.isNotEmpty ? NetworkImage(profileUrl) : null,
                          child: profileUrl.isEmpty ? const Icon(Icons.person, color: Colors.white30) : null,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          person['name'] ?? '',
                          textAlign: TextAlign.center,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w500),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          person['role'] ?? '',
                          textAlign: TextAlign.center,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(color: Colors.white54, fontSize: 11),
                        ),
                      ],
                    ),
                  );
                },
              ),
              if (_canScrollLeft)
                Positioned(
                  left: 0,
                  top: 0,
                  bottom: 30,
                  child: Center(
                    child: Container(
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.black.withValues(alpha: 0.6),
                      ),
                      child: IconButton(
                        icon: const Icon(Icons.chevron_left, color: Colors.white),
                        onPressed: _scrollLeft,
                      ),
                    ),
                  ),
                ),
              if (_canScrollRight)
                Positioned(
                  right: 0,
                  top: 0,
                  bottom: 30,
                  child: Center(
                    child: Container(
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.black.withValues(alpha: 0.6),
                      ),
                      child: IconButton(
                        icon: const Icon(Icons.chevron_right, color: Colors.white),
                        onPressed: _scrollRight,
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ],
    );
  }
}
"""

c += "\n" + horizontal_list_code

with open("lib/widgets/air_schedule_dialog.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Split logic into two components and added scroll controls!")
