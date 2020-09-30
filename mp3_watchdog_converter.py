import watchdog.events 
import watchdog.observers 
import time 
import os
import shutil
import subprocess
import subprocess as sp
import logging
import logging.handlers
import glob


def _convert(command,mp3_filename, logfile=True):
        """
        @param:
            command: command for conversion
        """
        if logfile:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)
            handler = logging.handlers.RotatingFileHandler(filename='requests.log', maxBytes=1024, backupCount=10)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        try:
            proc = sp.Popen(command, stdout=sp.PIPE,
                            bufsize=10**8)
            proc.wait()
            
            if proc.returncode:
                #err = "\n".join(["Audio conversion: %s\n" % cmd,
                #"WARNING: this command returned an error:",
                #err.decode('utf8')])
                #raise IOError(err)
                print("error")
                
            del proc
            
        except IOError as e:
            logger.error('{0}'.format(e), exc_info=True) 

        
def convert_to_mp3(path, filename): 

    codec = "libmp3lame"
    mp3_filename = filename + ".mp3"

    command = ["ffmpeg",
                   "-n",
                   "-i", path,
                   "-acodec", codec,
                   "-ab", "128k",
                   mp3_filename
                   ]

    return _convert(command,mp3_filename)

def getSize(path):
    if os.path.isfile(path): 
        st = os.stat(path)
        return st.st_size
    else:
        return -1

def wait_download(path,filename):
    current_size = getSize(path)
    print("File size")
    time.sleep(1)
    while current_size !=getSize(path) or getSize(path)==0:
        current_size =getSize(path)
        print("current_size:"+str(current_size))
        time.sleep(1)# wait download
    print("Downloaded")
    convert_to_mp3(path,filename)
 

class Handler(watchdog.events.PatternMatchingEventHandler): 
    def __init__(self): 
        # Set the patterns for PatternMatchingEventHandler 
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.m4a'], 
                                                             ignore_directories=True, case_sensitive=False) 
  
    def on_created(self, event): 
        print("Watchdog received created event - % s." % event.src_path) 
        path = event.src_path
        filename,ext = os.path.splitext(event.src_path)
        source = os.listdir("/home/pi/shared/Input/")

        wait_download(path,filename)

        dest = "/home/pi/shared/Output/"
        os.remove(filename+".m4a")

        for file in glob.glob("/home/pi/shared/Input/*.mp3"):
            shutil.move(file,dest)


    def on_modified(self, event): 
        print("Watchdog received modified event - % s." % event.src_path) 
        # Event is modified, you can process it now 
  
  
if __name__ == "__main__": 
    src_path = r"/home/pi/shared/Input/"
    event_handler = Handler() 
    observer = watchdog.observers.Observer() 
    observer.schedule(event_handler, path=src_path, recursive=True) 
    observer.start()
    print("Starting...")
    print("Watching: %s" %src_path )
    try: 
        while True: 
            time.sleep(1) 
    except KeyboardInterrupt: 
        observer.stop() 
    observer.join() 
