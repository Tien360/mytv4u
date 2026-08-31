[Setup]
ChangesAssociations=yes
AppName=MyTV4U
AppVersion=26.08.31.20.public
AppPublisher=Sparky
AppComments=MyTV4U - Ứng dụng xem phim trực tuyến đa nguồn (Yêu cầu cấp quyền Firewall cho tính năng phát Torrent/P2P)
DefaultDirName={autopf}\MyTV4U
DefaultGroupName=MyTV4U
UninstallDisplayIcon={app}\MyTV4U.exe
Compression=lzma2
SolidCompression=yes
OutputDir=T:\Project\Phim\mytv4u_flutter\Releases\v26.08.31.20.public
OutputBaseFilename=MyTV4U_Setup_26.08.31.20.public
SetupIconFile=T:\Project\Phim\mytv4u_flutter\windows\runner\resources\app_icon.ico

[Files]
Source: "T:\Project\Phim\mytv4u_flutter\build\windows\x64\runner\Release\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "vietnamese"; MessagesFile: "Vietnamese.isl"

[Icons]
Name: "{group}\MyTV4U"; Filename: "{app}\MyTV4U.exe"
Name: "{commondesktop}\MyTV4U"; Filename: "{app}\MyTV4U.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\MyTV4U.exe"; Description: "Launch MyTV4U"; Flags: nowait postinstall

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
Root: HKA; Subkey: "Software\Classes\MyTV4U.AudioFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}udio.ico"
Root: HKA; Subkey: "Software\Classes\MyTV4U.AudioFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: {app}\MyTV4U.exe %1

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
Root: HKA; Subkey: "Software\Classes\MyTV4U.VideoFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: {app}\MyTV4U.exe %1

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
