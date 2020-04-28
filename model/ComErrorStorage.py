from model.ComError import ComError
from model.ComErrorLogger import ComErrorLogger


class ComErrorStorage:

    def __init__(self):
        self.com_error_arr = []
        self.com_error_logger = ComErrorLogger()

    def add_error(self, err: ComError, total_packets=0):
        self.com_error_arr.append(err)
        err_total = self.get_err_total()
        self.com_error_logger.log_error(err, err_total, total_packets)

    def get_err_total(self):
        return len(self.com_error_arr)
