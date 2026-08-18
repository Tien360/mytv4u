import re

with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the condition if (enabledSources.contains('torrentio') && initialMovie != null) {
old_cond = "if (enabledSources.contains('torrentio') && initialMovie != null) {"
new_cond = "if ((enabledSources.contains('torrentio') || enabledSources.contains('vidsrc') || enabledSources.contains('vidapi')) && initialMovie != null) {"
content = content.replace(old_cond, new_cond)

# Patch EpisodeServer array for TV Shows
old_tv_servers = '''                    serversMap[9] = [
                      EpisodeServer(serverName: 'P2P (Torrent)', items: p2pItems),
                      if (vidsrcItems.isNotEmpty)
                        EpisodeServer(serverName: 'VidSrc (Embed)', items: vidsrcItems),
                      EpisodeServer(serverName: 'VidAPI (Embed)', items: vidApiItems),
                    ];'''
new_tv_servers = '''                    serversMap[9] = [
                      if (enabledSources.contains('torrentio')) EpisodeServer(serverName: 'P2P (Torrent)', items: p2pItems),
                      if (vidsrcItems.isNotEmpty && enabledSources.contains('vidsrc'))
                        EpisodeServer(serverName: 'VidSrc (Embed)', items: vidsrcItems),
                      if (enabledSources.contains('vidapi'))
                        EpisodeServer(serverName: 'VidAPI (Embed)', items: vidApiItems),
                    ];'''
content = content.replace(old_tv_servers, new_tv_servers)

# Patch TorrentioApi.fetchStreams
old_fetch = "final servers = await TorrentioApi.fetchStreams(imdbId);"
new_fetch = "final servers = enabledSources.contains('torrentio') ? await TorrentioApi.fetchStreams(imdbId) : <EpisodeServer>[];"
content = content.replace(old_fetch, new_fetch)

# Patch vidsrcServer
old_vidsrc_server = "final vidsrcServer = tmdbId != null ? EpisodeServer("
new_vidsrc_server = "final vidsrcServer = (tmdbId != null && enabledSources.contains('vidsrc')) ? EpisodeServer("
content = content.replace(old_vidsrc_server, new_vidsrc_server)

# Patch vidApiServer
old_vidapi_server = "final vidApiServer = EpisodeServer("
new_vidapi_server = "final vidApiServer = enabledSources.contains('vidapi') ? EpisodeServer("
content = content.replace(old_vidapi_server, new_vidapi_server)

# Patch servers.add(vidApiServer);
old_servers_add = "servers.add(vidApiServer);"
new_servers_add = "if (vidApiServer != null) servers.add(vidApiServer as EpisodeServer);"
content = content.replace(old_servers_add, new_servers_add)

# Patch fallback serversMap[9] array for movies
old_fallback = '''                  } else {
                    serversMap[9] = [
                      if (vidsrcServer != null) vidsrcServer,
                      vidApiServer
                    ];
                    processAndEmit();
                  }'''
new_fallback = '''                  } else {
                    serversMap[9] = [
                      if (vidsrcServer != null) vidsrcServer as EpisodeServer,
                      if (vidApiServer != null) vidApiServer as EpisodeServer,
                    ];
                    processAndEmit();
                  }'''
content = content.replace(old_fallback, new_fallback)

with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched phim_api.dart')
