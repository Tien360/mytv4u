with open('lib/screens/library_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("['mp4', 'mkv', 'avi', 'flv', 'webm', 'mov', 'ts']", "['mp4', 'mkv', 'avi', 'flv', 'webm', 'mov', 'ts', 'mp3', 'm4a', 'wav', 'flac', 'aac']")

with open('lib/screens/library_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated library_screen.dart to support audio files")
