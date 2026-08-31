path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_str = """      final isDesktop = MediaQuery.of(context).size.width >= 800;

    return Scaffold(
      backgroundColor: const Color(0xFF000000),
      drawer: isDesktop
          ? null
          : Drawer(
              backgroundColor: const Color(0xFF1A1A1A),
              child: SafeArea(child: _buildSidebarMenu()),
            ),
      body: Stack(
        children: [
          SafeArea("""

new_str = """      final isDesktop = MediaQuery.of(context).size.width >= 800;

    return Scaffold(
      backgroundColor: Colors.black,
      drawer: isDesktop
          ? null
          : Drawer(
              backgroundColor: const Color(0xFF1A1A1A),
              child: SafeArea(child: _buildSidebarMenu()),
            ),
      body: Stack(
        children: [
          const AmbientBackground(),
          SafeArea("""

if old_str in content:
    content = content.replace(old_str, new_str)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Could not find old_str")
