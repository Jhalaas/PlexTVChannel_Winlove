# DIY TV Channel for Plex

Ever wanted a personal 24/7 TV channel packed with your favorite shows and commercials? This project builds playlists and XMLTV guide data so you can stream through VLC, feed the channel into xTeVe, and watch it in Plex.

## ✨ Features
- Generate hour sized playlist blocks from show directories
- Optional commercial breaks
- Automatically build XMLTV guide data
- Windows GUI for easy configuration
- Automation scripts for Linux and Windows

## Table of Contents
1. [Requirements](#requirements)
2. [Windows Quick Start](#windows-quick-start)
3. [Linux Quick Start](#linux-quick-start)
4. [Detailed Setup](#detailed-setup)
5. [Automation](#automation)
6. [Support](#support)

## Requirements
- Plex with Plex Pass
- [xTeVe](https://xteve.de)
- VLC
- Python 3 with the packages in `requirements.txt`
- FFmpeg (required for moviepy on Windows and Linux)

## Windows Quick Start
1. Run `setup_windows.bat` once. It installs the Python packages, schedules the automation tasks, and creates a **PlexTVChannel_GUI** shortcut on your desktop.
2. Double‑click the shortcut to open the GUI.
3. Fill in your show directories and options, then click **Run**. The playlist and XMLTV files are generated automatically.

## Linux Quick Start
1. Edit `config.py` and populate the directory paths and channel information.
2. Run `python3 generatePlaylist.py no no` to build `playlist.m3u` and temporary guide files.
3. Run `python3 generateXMLTV.py` to create `xmltv.xml` from those temporary files.
4. Launch VLC with the generated playlist to start streaming.
5. Configure xTeVe to read the playlist and XMLTV guide, then add xTeVe as a DVR device in Plex.

### Windows Usage

Run **setup_windows.bat** once to install the required Python packages, schedule the automation tasks, and create a desktop shortcut. After the setup completes you can simply double click the **PlexTVChannel_GUI** shortcut on your desktop to open the graphical interface. The GUI lets you configure options and will update `config.py` before running `generatePlaylist.py` and `generateXMLTV.py` for you.

---

## Detailed Setup
### Playlist & Guide Generation
Populate these variables in `config.py` before running the scripts:
```python
cartoons = ["show1", "show2"]
dir = r"/path/to/shows/"
tvDirectory = r"/path/to/output/"
commercialsDirectory = r"/path/to/commercials/"
timezone = "-0400"
showPoster = "https://example/poster.png"
channelName = "My Channel"
```
Run the playlist generator with optional flags for backups and commercials:
```bash
python3 generatePlaylist.py <backup? (yes|no)> <commercials? (yes|no)>
python3 generateXMLTV.py
```
`generatePlaylist.py` creates `playlist.m3u` along with the temporary files
`temp_xmltv.xml` and `temp_variables.py`. Running `generateXMLTV.py` afterward
converts these temporary files into the final `xmltv.xml` guide.

### VLC Streaming
Start streaming the generated playlist over HTTP using VLC or `cvlc` on a headless server:
```bash
vlc -vvv /path/to/playlist.m3u --sout-keep --sout '#transcode{vcodec=h264,acodec=aac,vb=800,ab=128}:standard{access=http,mux=ts,dst=<ip:port>}' --sout-mux-caching=5000
```
If you copy this command and it fails to start, type it manually—quotation marks can be finicky.

### xTeVe Configuration
1. Launch xTeVe and add a new **Playlist** pointing to your VLC stream.
2. Add your generated `xmltv.xml` file under **XMLTV**.
3. Map the channel in the **Mapping** tab and select the XMLTV data.
4. Under **Settings**, change *Stream Buffer* to **VLC** and append `--loop` to the VLC options so the stream keeps running.

### Plex Integration
In Plex, go to **Live TV & DVR** and add a device using the IP and port of xTeVe. When prompted for a guide, browse to the `xmltv.xml` file. Finish the setup and your personal channel appears under Live TV.

---

## Automation
Automation scripts are provided for both Linux and Windows. Linux users can schedule
`tvStart.sh` and `tvContinue.sh` via `cron`, while Windows users can run the
equivalent PowerShell scripts `tvStart.ps1` and `tvContinue.ps1` with the Task
Scheduler. Running `setup_windows.bat` will create these scheduled tasks
automatically. All scripts need editing to match your paths and include an
example of refreshing the Plex guide using a Plex token.

## Support
This project was put together with love for the community. Donations are appreciated but certainly not required. [PayPal](https://paypal.me/tmurphy605)

Feel free to reach out with any questions.

— **Todd**

[My Website](http://toddamurphy.me/)
