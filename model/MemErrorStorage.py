from model.MemErrorData import MemErrorData
from model.MemErrorLogger import MemErrorLogger


class MemErrorStorage:

    def __init__(self):
        self.mem_error_arr = []
        self.mem_error_logger = MemErrorLogger()
        self.cnt = 0

    def add_error(self, err: str):
        err = MemErrorData(err, self.cnt)
        self.mem_error_arr.append(err)
        self.mem_error_logger.log_error(err)
        self.cnt += 1

    def get_err_total(self):
        return len(self.mem_error_arr)

    def get_mem_err(self, index: int):
        if index < len(self.mem_error_arr):
            return self.mem_error_arr[index]
        return None


