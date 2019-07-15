class Data:
    def __init__(self):
        self.data_payload = ""
        self.start_index = -1
        self.end_index = 0
        self.err_cnt = 0
        self.buff_len = 0
        self.len_of_hex = 0
        self.start_end_distance = -1
        self.data_pieces_num = 0

    def to_str(self):
        return vars(self)