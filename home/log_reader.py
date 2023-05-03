# Import Module
import os
import threading
import sys
from zoneinfo import ZoneInfo
from datetime import datetime
from mysite.settings import LOG_STRUCTURE_LIST as log_structure_list
from home.models import log

import signal

file_reading_threads = []

class LogReaderThread:
    def __init__(self, filepath):
        self._kill_pill = False
        self._thread = None

        self._last_pos = 0
        self._filepath = filepath
        self._values_dict = {}

    def start(self):
        self._thread = threading.Thread(target=self.read_log, args=())
        self._thread.start()

    def kill(self):
        print('Killing thread...')
        self._kill_pill = True

    def read_log(self):
        global log_structure_list
        while not self._kill_pill:
            self._values_dict = {}
            with open(self._filepath) as f:
                f.seek(self._last_pos)
                line = f.readline()
                while line:
                    for s in log_structure_list:
                        start = line.find('[')
                        end = line.find(']')
                        self._values_dict[s] = line[start+1:end]
                        line = line[end+1:]
                    self._values_dict['message'] = line.strip()
                    line = f.readline()
                    self.write_to_db()
                self._last_pos = f.tell()
    
    def write_to_db(self):
        timestamp = datetime.strptime(self._values_dict['timestamp'], '%y-%m-%d %H:%M:%S.%f')
        logs = log(timestamp=timestamp.replace(tzinfo=ZoneInfo('Asia/Kolkata')), application_name=self._values_dict['application_name'], level=self._values_dict['level'], message = self._values_dict['message'])
        logs.save()
        print(self._values_dict['timestamp'])

def start_all_log_reader_threads(root_dir):
    for file in os.listdir(root_dir):
        # Check whether file is in text format or not
        if not file.lower().endswith('.log'):
            continue
        file_path = r"C:\Users\User\Desktop\Alan\Projects\django-log-monitor\mysite\sample_logs"
        t = LogReaderThread(file_path)
        t.start()
        file_reading_threads.append(t)

def kill_all_log_reader_threads(signum, stack_frame):
    global file_reading_threads
    for ft in file_reading_threads:
        ft.kill()
    sys.exit(0)

signal.signal(signal.SIGINT, kill_all_log_reader_threads)