# Windows PowerShell script equivalent to tvContinue.sh
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$LockFile = Join-Path $env:TEMP "tvLockFile.lock"

# Wait until uptime is at least 10 minutes
$uptime = (Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
if ($uptime.TotalMinutes -lt 10) {
    Write-Host "Uptime has not reached 10 minutes!"
    exit 1
}

# Prevent concurrent runs
$startScriptRunning = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.Path -like '*tvStart.ps1' }
if ($startScriptRunning) {
    Write-Host "tvStart.ps1 running...exiting"
    exit 0
}

if (Test-Path $LockFile) {
    Write-Host "tvContinue.ps1 running...exiting"
    exit 1
}

if (Get-Process vlc -ErrorAction SilentlyContinue) {
    Write-Host "VLC running...exiting"
    exit 0
}

New-Item -ItemType File -Path $LockFile | Out-Null

python "$ScriptDir\generateXMLTV.py"
Start-Sleep -Seconds 2

Move-Item -Force "$ScriptDir\showList1.txt" "$ScriptDir\showList.txt"
Move-Item -Force "$ScriptDir\playlist1.m3u" "$ScriptDir\playlist.m3u"
Move-Item -Force "$ScriptDir\xmltv1.xml" "$ScriptDir\xmltv.xml"

Start-Sleep -Seconds 2

Write-Host "VLC stopped...starting it"
& "C:\Program Files\VideoLAN\VLC\vlc.exe" "$ScriptDir\playlist.m3u" --sout-keep --sout '#transcode{vcodec=h264, acodec=aac, vb=800, ab=128} :standard{access=http, mux=ts, dst=<ip:port>}' --sout-mux-caching=5000

Start-Sleep -Seconds 5
Write-Host ""
Start-Sleep -Seconds 2

python "$ScriptDir\generatePlaylist.py" yes no
Start-Sleep -Seconds 2

Remove-Item $LockFile

Invoke-WebRequest -Uri "https://<PlexServerIP>:32400/livetv/dvrs/<dvrID>/reloadGuide?X-Plex-Token=<api token>" -Method Post

