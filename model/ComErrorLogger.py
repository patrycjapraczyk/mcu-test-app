from model.Logger import Logger
from model.ComError import ComError
import time


class ComErrorLogger():
    FILE_NAME = 'com_errors.txt'

    def __init__(self):
        #self.start = self.get_curr_time()
        self.logger = Logger(self.FILE_NAME)
        self.start = self.logger.get_curr_time()

    def log_error(self, error: ComError, err_cnt, packets_received_num=1):
        freq = self.get_error_frequency(err_cnt, error.time)
        err_percent = self.get_error_ratio(packets_received_num, err_cnt)
        msg = '\n' + str(err_cnt) + '. ' + error.type
        msg += ' for ' + error.packet + '\n'
        msg += 'STATS: time: ' + str(error.time)
        msg += ', error percentage: ' + str(err_percent) + '*10^(-4)%,\n'
        msg += 'error frequency: ' + freq

    def get_error_ratio(self, err_cnt, packets_received_num=1):
        MULTIPLY_FACTOR = 1000000
        percent = (MULTIPLY_FACTOR * err_cnt) / (packets_received_num + err_cnt)
        return percent

    def get_error_frequency(self, err_cnt, end):
        elapsed_time = (end - self.start)
        if elapsed_time > 0:
            freq = (err_cnt / elapsed_time) * 1000
            freq = str(freq) + 'GHz'
        else:
            freq = ' <infinite frequency> '
        return freq

    def get_curr_time(self):
        # TODO: define which freq units suit the current usecase
        return time.time_ns()  # return the current time in nano_seconds since the Epoch
