from model.Logger import Logger
from model.ComError import ComError
from model.Time import Time


class ComErrorLogger:
    FILE_NAME = 'com_errors.txt'

    def __init__(self):
        #self.start = self.get_curr_time()
        self.logger = Logger(self.FILE_NAME)
        self.start = Time.get_curr_time_ns()
        self.logger.log(' COMMUNICATION ERRORS:\n')

    def log_error(self, error: ComError, err_cnt, packets_received_num=1):
        err_percent = self.get_error_percentage(err_cnt, packets_received_num)
        msg = '\n' + str(err_cnt) + '. ' + error.type
        msg += ' for ' + error.packet + '\n'
        msg += 'STATS: time: ' + str(Time.get_curr_time())
        msg += ', error percentage: ' + str(err_percent) + '*10^(-3)%,\n'
        freq = self.get_error_frequency(err_cnt, error.time)
        msg += 'error frequency: ' + freq
        msg += error.extra_data
        self.logger.log(msg)


    def get_error_percentage(self, err_cnt, packets_received_num):
        MULTIPLY_FACTOR = 100000
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