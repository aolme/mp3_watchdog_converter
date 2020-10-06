Runs a Python Watchdog on a Raspberry Pi network shared Samba folder. When .m4a files are uploaded to the Input folder it converts them to .MP3's and moves them to the Output folder.

The watchdog script needs to be running in a terminal. I created an autostart shell script that launches a terminal window and starts the watchdog after login. Add the line from lxsession_autostart.txt in /etc/xdg/lxsession/LXDE-pi/autostart
