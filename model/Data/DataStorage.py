from model.Data.Data import Data
from model.Data.MemErrorStorage import MemErrorStorage
from model.StaticClasses.Time import Time
from model.StaticClasses.GlobalConstants import GlobalConstants


class DataStorage:

    def __init__(self):
        self.prev_data = None
        self.data_arr = []
        self.mem_error_storage = MemErrorStorage()
        self.curr_data = Data()
        self.last_heartbeat = None
        self.data_cnt = 0

    def save_curr_data(self):
        """"
            adds self.curr_data to self.data_arr with a timestamp
            if it is not heartbeat

            creates a memory_error and adds it self.mem_errors
            if self.curr_data.msg_code == 'ECC_CHECKED'

            clears self.curr_data
        """
        curr_time = str(Time.get_curr_time())
        self.curr_data.time = curr_time

        self.curr_data.extract_data_payload()

        #add end index
        self.curr_data.data_payload += GlobalConstants.END_CODE
        self.curr_data.complete_data += GlobalConstants.END_CODE

        print(str(curr_time) + ' saving data: ' + self.curr_data.complete_data)

        data_type = self.curr_data.purpose
        if not data_type == 'HEARTBEAT':
            self.data_arr.append(self.curr_data)
        if data_type == 'ECC_CHECKED':
            self.mem_error_storage.add_error(self.curr_data.data_payload_value)

        self.curr_data.payload_len = len(self.curr_data.data_payload)
        self.data_cnt += 1
        self.prev_data = self.curr_data
        self.curr_data = Data()

    def reset_curr_data(self):
        self.prev_data = Data()
        self.curr_data = Data()

    def get_data(self, id):
        for data in self.data_arr:
            if data.data_index == id:
                return data
        return None