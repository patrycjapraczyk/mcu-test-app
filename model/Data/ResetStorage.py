from model.Logging.ResetLogger import ResetLogger
from model.Data.ResetData import ResetData


class ResetStorage:
    def __init__(self):
        self.reset_arr = []
        self.reset_logger = ResetLogger()

    def add(self, reset_packet: ResetData):
        cnt = len(self.reset_arr)
        self.reset_logger.log(reset_packet, cnt)
        self.reset_arr.append(reset_packet)


