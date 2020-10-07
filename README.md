Converts downloaded YouTube .m4a audio files from my iPhone into .mp3 files on my home network.

Runs a Python Watchdog on a Raspberry Pi network shared Samba folder. When .m4a files are uploaded to the Input folder it converts them to .MP3's and moves them to the Output folder.

You need to compile ffmpeg in order to enable libmp3lame.

The watchdog script needs to be running in a terminal. I created an autostart shell script that launches a terminal window and starts the watchdog after login. Add the line from lxsession_autostart.txt in /etc/xdg/lxsession/LXDE-pi/autostart
in run at boot time.
