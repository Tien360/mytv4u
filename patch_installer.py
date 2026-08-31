path = r"T:\Project\Phim\mytv4u_flutter\installer.iss"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add audio.ico to Files
file_section = """[Files]
Source: "T:\Project\Phim\mytv4u_flutter\build\windows\x64\runner\Release\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs"""

new_file_section = file_section + """
Source: "T:\Project\Phim\mytv4u_flutter\windows\runner\resources\audio.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "T:\Project\Phim\mytv4u_flutter\windows\runner\resources\app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion"""

content = content.replace(file_section, new_file_section)

# 2. Add Registry section at the end
registry_section = """
[Registry]
; App Path so Windows knows where MyTV4U.exe is
Root: HKA; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\MyTV4U.exe"; ValueType: string; ValueName: ""; ValueData: "{app}\MyTV4U.exe"; Flags: uninsdeletekey
Root: HKA; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\MyTV4U.exe"; ValueType: string; ValueName: "Path"; ValueData: "{app}"

; ==========================
; AUDIO FILES (Uses audio.ico)
; ==========================
Root: HKA; Subkey: "Software\Classes\.mp3"; ValueType: string; ValueName: ""; ValueData: "MyTV4U.AudioFile"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\.wav"; ValueType: string; ValueName: ""; ValueData: "MyTV4U.AudioFile"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\.flac"; ValueType: string; ValueName: ""; ValueData: "MyTV4U.AudioFile"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\.aac"; ValueType: string; ValueName: ""; ValueData: "MyTV4U.AudioFile"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\.m4a"; ValueType: string; ValueName: ""; ValueData: "MyTV4U.AudioFile"; Flags: uninsdeletevalue

Root: HKA; Subkey: "Software\Classes\MyTV4U.AudioFile"; ValueType: string; ValueName: ""; ValueData: "MyTV4U Audio File"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\MyTV4U.AudioFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\audio.ico"
Root: HKA; Subkey: "Software\Classes\MyTV4U.AudioFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """"{app}\MyTV4U.exe"" ""%1""""

; ==========================
; VIDEO FILES (Uses app_icon.ico or MyTV4U.exe,0)
; ==========================
Root: HKA; Subkey: "Software\Classes\.mp4"; ValueType: string; ValueName: ""; ValueData: "MyTV4U.VideoFile"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\.mkv"; ValueType: string; ValueName: ""; ValueData: "MyTV4U.VideoFile"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\.avi"; ValueType: string; ValueName: ""; ValueData: "MyTV4U.VideoFile"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\.webm"; ValueType: string; ValueName: ""; ValueData: "MyTV4U.VideoFile"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\.mov"; ValueType: string; ValueName: ""; ValueData: "MyTV4U.VideoFile"; Flags: uninsdeletevalue

Root: HKA; Subkey: "Software\Classes\MyTV4U.VideoFile"; ValueType: string; ValueName: ""; ValueData: "MyTV4U Video File"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\MyTV4U.VideoFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\MyTV4U.exe,0"
Root: HKA; Subkey: "Software\Classes\MyTV4U.VideoFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """"{app}\MyTV4U.exe"" ""%1""""

; ==========================
; Register as a Windows "Default Apps" Candidate
; ==========================
Root: HKA; Subkey: "Software\MyTV4U\Capabilities"; ValueType: string; ValueName: "ApplicationDescription"; ValueData: "MyTV4U - Ung dung xem phim va phat Media chuyen nghiep"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\MyTV4U\Capabilities"; ValueType: string; ValueName: "ApplicationName"; ValueData: "MyTV4U"
Root: HKA; Subkey: "Software\MyTV4U\Capabilities\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\MyTV4U.exe,0"

Root: HKA; Subkey: "Software\MyTV4U\Capabilities\FileAssociations"; ValueType: string; ValueName: ".mp3"; ValueData: "MyTV4U.AudioFile"
Root: HKA; Subkey: "Software\MyTV4U\Capabilities\FileAssociations"; ValueType: string; ValueName: ".wav"; ValueData: "MyTV4U.AudioFile"
Root: HKA; Subkey: "Software\MyTV4U\Capabilities\FileAssociations"; ValueType: string; ValueName: ".flac"; ValueData: "MyTV4U.AudioFile"
Root: HKA; Subkey: "Software\MyTV4U\Capabilities\FileAssociations"; ValueType: string; ValueName: ".aac"; ValueData: "MyTV4U.AudioFile"
Root: HKA; Subkey: "Software\MyTV4U\Capabilities\FileAssociations"; ValueType: string; ValueName: ".m4a"; ValueData: "MyTV4U.AudioFile"

Root: HKA; Subkey: "Software\MyTV4U\Capabilities\FileAssociations"; ValueType: string; ValueName: ".mp4"; ValueData: "MyTV4U.VideoFile"
Root: HKA; Subkey: "Software\MyTV4U\Capabilities\FileAssociations"; ValueType: string; ValueName: ".mkv"; ValueData: "MyTV4U.VideoFile"
Root: HKA; Subkey: "Software\MyTV4U\Capabilities\FileAssociations"; ValueType: string; ValueName: ".avi"; ValueData: "MyTV4U.VideoFile"
Root: HKA; Subkey: "Software\MyTV4U\Capabilities\FileAssociations"; ValueType: string; ValueName: ".webm"; ValueData: "MyTV4U.VideoFile"
Root: HKA; Subkey: "Software\MyTV4U\Capabilities\FileAssociations"; ValueType: string; ValueName: ".mov"; ValueData: "MyTV4U.VideoFile"

Root: HKA; Subkey: "Software\RegisteredApplications"; ValueType: string; ValueName: "MyTV4U"; ValueData: "Software\MyTV4U\Capabilities"; Flags: uninsdeletevalue
"""

if "[Registry]" not in content:
    content += registry_section

# 3. Add ChangesEnvironment flag to Setup section so Explorer refreshes icons
if "ChangesEnvironment=yes" not in content:
    content = content.replace("[Setup]\n", "[Setup]\nChangesAssociations=yes\n")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated installer.iss with File Associations")
