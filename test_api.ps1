[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$slug = "toa-sang-nhu-nhung-vi-sao"
$ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

function Get-Json {
    param([string]$Url)
    $wc = New-Object System.Net.WebClient
    $wc.Headers.Add("User-Agent", $ua)
    $wc.Encoding = [System.Text.Encoding]::UTF8
    return $wc.DownloadString($Url) | ConvertFrom-Json
}

Write-Host "=== NguonC episode structure ==="
try {
    $j = Get-Json "https://phim.nguonc.com/api/film/$slug"
    $ep0 = $j.movie.episodes[0]
    Write-Host "  server_name:" $ep0.server_name
    $epKeys = $ep0.PSObject.Properties.Name -join ", "
    Write-Host "  ep0 keys:" $epKeys
    
    # Check items vs server_data
    if ($ep0.server_data) {
        $sd0 = $ep0.server_data[0]
        Write-Host "  server_data[0] keys:" ($sd0.PSObject.Properties.Name -join ", ")
        Write-Host "  server_data[0]:" ($sd0 | ConvertTo-Json -Compress)
    }
    if ($ep0.items) {
        $it0 = $ep0.items[0]
        Write-Host "  items[0] keys:" ($it0.PSObject.Properties.Name -join ", ")
        Write-Host "  items[0]:" ($it0 | ConvertTo-Json -Compress)
    }
} catch { Write-Host "  ERR:" $_.Exception.Message }

Write-Host ""
Write-Host "=== KKPhim episode structure ==="
try {
    $j = Get-Json "https://ophim1.com/v1/api/phim/$slug"
    $item = $j.data.item
    Write-Host "  item keys:" ($item.PSObject.Properties.Name -join ", ")
    if ($item.episodes) {
        $ep0 = $item.episodes[0]
        Write-Host "  episodes[0] keys:" ($ep0.PSObject.Properties.Name -join ", ")
        Write-Host "  server_name:" $ep0.server_name
        if ($ep0.server_data) {
            Write-Host "  server_data[0] keys:" ($ep0.server_data[0].PSObject.Properties.Name -join ", ")
            Write-Host "  server_data[0]:" ($ep0.server_data[0] | ConvertTo-Json -Compress)
        }
        if ($ep0.items) {
            Write-Host "  items[0]:" ($ep0.items[0] | ConvertTo-Json -Compress)
        }
    }
} catch { Write-Host "  ERR:" $_.Exception.Message }

Write-Host ""
Write-Host "=== Premium episode structure ==="
try {
    $j = Get-Json "https://dogtail.oxaliplatin.workers.dev/api/premium/detail/$slug"
    $ep0 = $j.movie.episodes[0]
    Write-Host "  server_name:" $ep0.server_name
    Write-Host "  ep0 keys:" ($ep0.PSObject.Properties.Name -join ", ")
    if ($ep0.server_data) {
        Write-Host "  server_data[0] keys:" ($ep0.server_data[0].PSObject.Properties.Name -join ", ")
        Write-Host "  server_data[0]:" ($ep0.server_data[0] | ConvertTo-Json -Compress)
    }
    if ($ep0.items) {
        Write-Host "  items[0]:" ($ep0.items[0] | ConvertTo-Json -Compress)
    }
} catch { Write-Host "  ERR:" $_.Exception.Message }

Write-Host ""
Write-Host "=== Free1 episode structure ==="
try {
    $j = Get-Json "https://free1.phim4k.lol/v1/api/phim/$slug"
    $item = $j.data.item
    if ($item.episodes) {
        $ep0 = $item.episodes[0]
        Write-Host "  episodes[0] keys:" ($ep0.PSObject.Properties.Name -join ", ")
        Write-Host "  server_name:" $ep0.server_name
        if ($ep0.server_data) {
            Write-Host "  server_data[0]:" ($ep0.server_data[0] | ConvertTo-Json -Compress)
        }
        if ($ep0.items) {
            Write-Host "  items[0]:" ($ep0.items[0] | ConvertTo-Json -Compress)
        }
    }
} catch { Write-Host "  ERR:" $_.Exception.Message }
