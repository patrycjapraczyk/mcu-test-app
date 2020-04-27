from model.Data import Data


class DataStorage:
    def __init__(self):
        self.prev_data = None
        self.data_arr = []
        self.curr_data = Data()
        self.data_cnt = 0

    def save_curr_data(self):
        """"
            adds self.curr_data to self._data_arr
            and clears self.curr_data
        """
        if not self.curr_data.msg_code == 'HEARTBEAT':
            self.data_arr.append(self.curr_data)
        self.curr_data.payload_len = len(self.curr_data.data_payload)
        self.data_cnt += 1
        self.prev_data = self.curr_data
        self.curr_data = Data()
