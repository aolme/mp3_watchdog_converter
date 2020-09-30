#script to launch lxterminal and start the watchdog.
#!/bin/bash
lxterminal -e bash -c 'python3 /home/pi/scripts/mp3_watchdog_converter.py; bash'
