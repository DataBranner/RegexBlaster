#! /usr/bin/python
# timer.py
# David Prager Branner
# 20140410

import time
import datetime

class Timer():
    def __init__(self, time_limit=None):
        self.start_time = time.time()
        self.time_limit = time_limit # If we are timing games.
        self.update()

    def update(self):
        self.time_passed = time.time() - self.start_time
        if self.time_limit:
            self.time_to_display = self.time_limit - self.time_passed
        else:
            self.time_to_display = self.time_passed
        self.time_to_display_str = str(
                datetime.timedelta(seconds=round(self.time_to_display)))
        if self.time_to_display_str[0:5] == '0:00:':
            self.time_to_display_str = self.time_to_display_str[5:]
        elif self.time_to_display_str[0:2] == '0:':
            self.time_to_display_str = self.time_to_display_str[2:]
        if self.time_to_display_str[0] == '0':
            self.time_to_display_str = self.time_to_display_str[1:]

