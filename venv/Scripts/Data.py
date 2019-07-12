class Data:
    def __init__(self):
        self.data_payload = ""
        self.start_index = -1
        self.end_index = -1
        self.err_cnt = 0
        self.buff_len = 0
        self.len_of_hex = 0
        self.start_end_distance = -1

    def to_str(self):
        return vars(self)