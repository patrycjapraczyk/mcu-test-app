from model.Time import Time
from model.Logger import Logger
from model.MemErrorData import MemErrorData


class MemErrorLogger:
    FILE_NAME = 'mem_errors.txt'

    def __init__(self):
        #self.start = self.get_curr_time()
        self.logger = Logger(self.FILE_NAME)
        self.start = Time.get_curr_time_ns()
        self.logger.log('MEMORY ERRORS:\n')

    def log_error(self, error: MemErrorData):
        msg = '\n[' + str(error.mem_error_id) + '] '
        msg += 'error number: ' + str(error.error_num)
        msg += ', overflow:  ' + str(error.overflow) + '\n'
        msg += ', faulty addresses: \n'
        for faulty_addr in error.faulty_addresses:
            msg += faulty_addr + ' '
        msg += '\n STATS: time: ' + str(error.time)
        self.logger.log(msg)

