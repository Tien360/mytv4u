import re

with open("lib/api/phim_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the incorrect end of fetchPremium
old_end = """            serversMap[5] = premiumServers;
            processAndEmit();
        }
    }
    
    
      if (enabledSources.contains('motchill')) {"""

new_end = """            serversMap[5] = premiumServers;
            processAndEmit();
        }
    }
    
    futures.add(fetchPremium());
  }
      
  if (enabledSources.contains('motchill')) {"""

content = content.replace(old_end, new_end)

with open("lib/api/phim_api.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("phim_api.dart brace fixed")
