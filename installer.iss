[Setup]
AppName=MyTV4U
AppVersion=26.08.08.a.public
DefaultDirName={autopf}\MyTV4U
DefaultGroupName=MyTV4U
UninstallDisplayIcon={app}\mytv4u_flutter.exe
Compression=lzma2
SolidCompression=yes
OutputDir=T:\Project\Phim\mytv4u_flutter\build\windows\x64\runner\Release
OutputBaseFilename=setup
SetupIconFile=T:\Project\Phim\mytv4u_flutter\windows\runner\resources\app_icon.ico

[Files]
Source: "T:\Project\Phim\mytv4u_flutter\build\windows\x64\runner\Release\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\MyTV4U"; Filename: "{app}\mytv4u_flutter.exe"
Name: "{commondesktop}\MyTV4U"; Filename: "{app}\mytv4u_flutter.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"
