import time
import datetime
from FileManager import FileManager


class ErrorLogger:
    FILE_NAME = 'errors.txt'

    def __init__(self):
        self.err_cnt = 0
        self.f_manager = FileManager(self.FILE_NAME)
        self.log_start()
        self.start = self.get_curr_time()
        i = 0

    def get_curr_time(self):
        # TODO: define which freq units suit the current usecase
        return time.time_ns()  # return the current time in nano_seconds since the Epoch

    def log_error(self, msg, packets_received_num=1):
        self.err_cnt += 1
        curr_time = self.get_curr_time()
        freq = self.get_error_frequency()
        err_percent = self.get_error_percentage(packets_received_num)
        msg = '\n' + str(self.err_cnt) + '. ' + msg + '\n'
        msg += 'STATS: time: ' + str(curr_time)
        msg += ', error percentage: ' + str(err_percent) + '*10^(-4)%,\n'
        msg += 'error frequency: ' + self.get_error_frequency()
        self.f_manager.file_write(msg)

    def log_start(self):
        date = str(datetime.datetime.now())
        self.f_manager.file_write("\nStarted at: " + date)

    def log_end(self):
        date = str(datetime.datetime.now())
        self.f_manager.file_write("\nEnded at: " + date)

    def get_error_percentage(self, packets_received_num=1):
        MULTIPLY_FACTOR = 1000000
        percent = (MULTIPLY_FACTOR * self.err_cnt) / (packets_received_num + self.err_cnt)
        return percent

    def get_error_frequency(self):
        end = self.get_curr_time()
        elapsed_time = (end - self.start)
        if elapsed_time > 0:
            freq = (self.err_cnt / elapsed_time) * 1000
            freq = str(freq) + 'GHz'
        else:
            freq = ' <infinite frequency> '
        return freq

# TEST
# logger = ErrorLogger()
# logger.log_error("LOL", 1)
# time.sleep(1)
# logger.log_error("LOL2", 2)
