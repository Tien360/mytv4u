Add-Type -AssemblyName System.IO.Compression.FileSystem

$sourceDir = "t:\Project\Phim\mytv4u_flutter"
$destZip = "t:\Project\Phim\mytv4u_flutter_backup_26.09.14.30.zip"

if (Test-Path $destZip) {
    Remove-Item $destZip
}

$tempDir = "t:\Project\Phim\mytv4u_flutter_temp"
if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

Copy-Item -Path "$sourceDir\*" -Destination $tempDir -Recurse -Exclude "build", ".dart_tool", ".pub-cache", ".git", "Releases", "windows\flutter\ephemeral" -Force

[System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $destZip)

Remove-Item $tempDir -Recurse -Force
Write-Host "Backup created at $destZip"
