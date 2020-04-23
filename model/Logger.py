import time
import datetime
from abc import abstractmethod

from model.FileManager import FileManager


class Logger:

    def __init__(self, FILE_NAME):
        self.f_manager = FileManager(FILE_NAME)
        self.log_start()
        i = 0

    @abstractmethod
    def log(self, msg):
        self.f_manager.file_write(msg)

    def get_curr_time(self):
        # TODO: define which freq units suit the current usecase
        return time.time_ns()  # return the current time in nano_seconds since the Epoch

    def log_start(self):
        date = str(datetime.datetime.now())
        self.f_manager.file_write("\nStarted at: " + date)