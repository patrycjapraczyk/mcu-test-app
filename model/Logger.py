from model.Time import Time
from model.FileManager import FileManager


class Logger:

    def __init__(self, FILE_NAME):
        self.f_manager = FileManager(FILE_NAME)
        self.log_start()
        i = 0

    def log(self, msg):
        self.f_manager.file_write(msg)

    def log_start(self):
        date = str(Time.get_curr_time())
        self.f_manager.file_write("\nStarted at: " + date)
