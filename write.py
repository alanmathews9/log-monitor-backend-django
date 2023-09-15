import time
import threading
import signal
import sys
from datetime import datetime
import random

kill_pill = False   

# to kill the thread, and stop writing to the file
def set_kill_pill(signum, frame):
    global kill_pill
    kill_pill = True
    sys.exit(0)


signal.signal(signal.SIGINT, set_kill_pill) # we kill thread on SIGINT signal

log_msg_list = [ ['WARNING', 'This is a warning message'], ['ERROR', 'This is one error msg'], ['CRITICAL', 'This is a CRITICAL']]
# appllication_list = ['AppServer', 'StrategyServer', 'NodeServer', 'Algo']

print('Enter Application name: ')
application = input()

# function to write to the file
def file_writer(file_path):
    global kill_pill
    while True: 
        now = datetime.now() # current date and time
        localtime=now.strftime("%y-%m-%d %H:%M:%S.%f")
        level, msg = random.choice(log_msg_list)
        # application = random.choice(appllication_list)
        logs='['+ localtime +'] [' + application + '] [' + level + '] ' + msg
        f=open(file_path,"a")   # open the file in append mode
        f.write(logs)           # write to the file
        f.write('\n')           # write a new line
        f.close()
        time.sleep(10)          # sleep for 10 seconds, and then write to the file again
        #print(kill_pill)
        if kill_pill:           # if kill_pill is True, then break out of the loop and stop writing to the file
            break

file_path = 'sample_logs/' + application +'.log'
t = threading.Thread(target=file_writer, args=(file_path,))
t.start()
a = input()
set_kill_pill()
# t.join()