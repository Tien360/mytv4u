import os
import json
import urllib.request
import urllib.error

# Extract all links from next_episode_tracker.dart
import re

with open("lib/widgets/next_episode_tracker.dart", "r", encoding="utf-8") as f:
    text = f.read()

urls = re.findall(r"'(https://assets[0-9]+\.lottiefiles\.com/[^']+)'", text)

os.makedirs("assets/lottie", exist_ok=True)

success_count = 0
for url in set(urls):
    filename = url.split("/")[-1]
    filepath = os.path.join("assets/lottie", filename)
    if not os.path.exists(filepath):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
            success_count += 1
            # Update the dart file to point to the local asset
            text = text.replace(url, f"assets/lottie/{filename}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            # If fail, replace with a known working or fallback emoji text?
            pass

# Write updated dart file
with open("lib/widgets/next_episode_tracker.dart", "w", encoding="utf-8") as f:
    f.write(text)

print(f"Downloaded {success_count} lottie files.")
