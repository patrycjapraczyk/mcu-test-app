from model.Logging.Logger import Logger
from model.StaticClasses.Time import Time
from model.Data.ResetData import ResetData


class ResetLogger:
    FILE_NAME = 'reset.txt'

    def __init__(self):
        # self.start = self.get_curr_time()
        self.logger = Logger(self.FILE_NAME)
        self.logger.log('RESET PACKETS:\n')

    def log(self, reset: ResetData, cnt: int):
        msg = '\n[' + str(cnt) + '] '
        msg += 'RESET PURPOSE: ' + reset.type + '\n'
        msg += 'STATS: time: ' + str(Time.get_curr_time())
        self.logger.log(msg)