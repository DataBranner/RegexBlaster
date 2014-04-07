#! /usr/bin/python
# timer.py
# David Prager Branner
# 20140407

import time
import datetime

class Timer():
    def __init__(self, time_limit=300):
        self.start_time = time.time()
        self.time_limit = time_limit
        self.update()

    def update(self):
        self.time_passed = time.time() - self.start_time
        self.time_left = self.time_limit - self.time_passed
        self.time_left_str = str(
                datetime.timedelta(seconds=round(self.time_left)))
        if self.time_left_str[0:5] == '0:00:':
            self.time_left_str = self.time_left_str[5:]
        elif self.time_left_str[0:2] == '0:':
            self.time_left_str = self.time_left_str[2:]
        if self.time_left_str[0] == '0':
            self.time_left_str = self.time_left_str[1:]

