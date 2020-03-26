from Data import Data


class DataStorage:
    def __init__(self):
        self.data_arr = []
        self.curr_data = Data()
        self.data_cnt = 0

    def save_curr_data(self):
        """"
            adds self.curr_data to self._data_arr
            and clears self.curr_data
        """
        self.data_arr.append(self.curr_data)
        self.curr_data.payload_len = len(self.curr_data.data_payload)
        self.data_cnt += 1
        self.curr_data = Data()

    def print_all_data(self) -> str:
        data_str = ""
        for data in self.data_arr:
            data_str += data.to_str()
        return data_str
