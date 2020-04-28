from model.MemErrorData import MemErrorData
from model.MemErrorLogger import MemErrorLogger


class MemErrorStorage:

    def __init__(self):
        self.mem_error_arr = []
        self.mem_error_logger = MemErrorLogger()

    def add_error(self, err: str):
        err = MemErrorData(str)
        self.mem_error_arr.append(err)
        self.mem_error_logger.log_error(err)

    def get_err_total(self):
        return len(self.mem_error_arr)


