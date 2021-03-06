from model.Data.ComError import ComError
from model.Logging.ComErrorLogger import ComErrorLogger


class ComErrorStorage:

    def __init__(self):
        self.com_error_arr = []
        self.com_error_logger = ComErrorLogger()

    def add(self, err: ComError, total_packets=0):
        self.com_error_arr.append(err)
        err_total = self.get_err_total()
        self.com_error_logger.log_error(err, err_total, total_packets)

    def get_err_total(self):
        return len(self.com_error_arr)

    def get_error_percentage(self, total_packets):
        percent = ComErrorLogger.get_error_percentage(self.get_err_total(), total_packets)
        percent = int(percent/1000)
        return percent

    def end(self, total_packets):
        self.com_error_logger.log_end(total_packets)
