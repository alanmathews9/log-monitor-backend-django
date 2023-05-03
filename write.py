import time
import threading
import signal
import sys
from datetime import datetime

kill_pill = False

def set_kill_pill():
    global kill_pill
    kill_pill = True
    sys.exit(0)


signal.signal(signal.SIGINT, set_kill_pill)

def file_writer(file_path):
    global kill_pill
    while True:
        now = datetime.now() # current date and time
        localtime=now.strftime("%y-%m-%d %H:%M:%S.%f")
        logs='['+localtime+']'+'[SS] [CRITICAL] Created new connection and added it to registry. Going to start communication on connection. Connection: 13'
        f=open(file_path,"a")
        f.write(logs)
        f.write('\n')
        f.close()
        time.sleep(10)
        #print(kill_pill)
        if kill_pill:
            break

file_path = "django-log-monitor/mysite/sample_logs/sample_log.log"
t = threading.Thread(target=file_writer, args=(file_path,))
t.start()
a = input()
set_kill_pill()
# t.join()