import os
import threading
import sys
from zoneinfo import ZoneInfo
from datetime import datetime
from mysite.settings import LOG_STRUCTURE_LIST as log_structure_list
from home.models import log

import signal

# WE NEED THREADING HERE BECAUSE WE WANT TO READ MULTIPLE LOG FILES CONCURRENTLY

file_reading_threads = []

class LogReaderThread:
    def __init__(self, filepath):
        self._kill_pill = False
        self._thread = None

        self._last_pos = 0
        self._filepath = filepath
        self._values_dict = {}

    # the Thread class is used to create a thread so we can run multiple functions concurrently
    # the function the thread should execute is the read_log function
    # the start method is used to start the thread
    def start(self):
        self._thread = threading.Thread(target=self.read_log, args=())  
        self._thread.start()

    # to kill the thread
    def kill(self):
        print('Killing thread...')
        self._kill_pill = True

    def read_log(self):
        global log_structure_list
        while not self._kill_pill:
            self._values_dict = {}
            with open(self._filepath) as f: # open the file
                f.seek(self._last_pos)      # seek to the last position
                line = f.readline()         # read the last line
                while line:     
                    # parse the line and store the values in a dictionary
                    for s in log_structure_list:    
                        start = line.find('[')
                        end = line.find(']')
                        self._values_dict[s] = line[start+1:end]
                        line = line[end+1:]
                    self._values_dict['message'] = line.strip() # the remaining part of the line is the message
                    line = f.readline()
                    self.write_to_db()  # to read values in _values_dict and write it to the database
                self._last_pos = f.tell()   # update the last position
    
    # takes in a dictionary of values (_values_dict) and writes it to the database (log table
    def write_to_db(self):
        timestamp = datetime.strptime(self._values_dict['timestamp'], '%y-%m-%d %H:%M:%S.%f')
        logs = log(timestamp=timestamp.replace(tzinfo=ZoneInfo('Asia/Kolkata')), application_name=self._values_dict['application_name'], level=self._values_dict['log_level'], message = self._values_dict['message'])
        logs.save()
        print(self._values_dict['timestamp'])

# starts all the log reader threads for all .log files in the root directory
def start_all_log_reader_threads(root_dir):
    for file in os.listdir(root_dir):
        # Check whether file is in correct format of not
        if not file.lower().endswith('.log'):
            continue
        file_path = f"{root_dir}\{file}"
        t = LogReaderThread(file_path)
        t.start()
        file_reading_threads.append(t)  # append the thread to the list of threads

# it calls the kill method for all threads in file_reading_threads list
def kill_all_log_reader_threads(signum, stack_frame):
    global file_reading_threads
    for ft in file_reading_threads:
        ft.kill()
    sys.exit(0)     

signal.signal(signal.SIGINT, kill_all_log_reader_threads)   # sets the signal handler for SIGINT signal to kill_all_log_reader_threads function