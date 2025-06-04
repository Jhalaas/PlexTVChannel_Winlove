# Windows PowerShell script equivalent to tvStart.sh
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "Generating playlist for Todderang"

python "$ScriptDir\generatePlaylist.py" no no
Start-Sleep -Seconds 5

python "$ScriptDir\generateXMLTV.py"
Start-Sleep -Seconds 2

Invoke-WebRequest -Uri "https://<PlexServerIP>:32400/livetv/dvrs/<dvrID>/reloadGuide?X-Plex-Token=<api token>" -Method Post
Start-Sleep -Seconds 2

& "C:\Program Files\VideoLAN\VLC\vlc.exe" "$ScriptDir\playlist.m3u" --sout-keep --sout '#transcode{vcodec=h264, acodec=aac, vb=800, ab=128} :standard{access=http, mux=ts, dst=<ip:port>}' --sout-mux-caching=5000

Start-Sleep -Seconds 5
Write-Host ""
Start-Sleep -Seconds 2

python "$ScriptDir\generatePlaylist.py" yes no

