[Setup]
AppName=MyTV4U
AppVersion=26.08.18.f.beta
AppPublisher=Sparky
AppComments=MyTV4U - Ứng dụng xem phim trực tuyến đa nguồn (Yêu cầu cấp quyền Firewall cho tính năng phát Torrent/P2P)
DefaultDirName={autopf}\MyTV4U
DefaultGroupName=MyTV4U
UninstallDisplayIcon={app}\MyTV4U.exe
Compression=lzma2
SolidCompression=yes
OutputDir=T:\Project\Phim\mytv4u_flutter\Releases\v26.08.18.f.beta
OutputBaseFilename=MyTV4U_Setup_26.08.18.f.beta
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
