class Data:
    def __init__(self):
        self.data_payload = ""
        self.payload_len = 0
        self.err_cnt = 0
        self.buff_len = 0
        self.len_of_hex = 0
        self.data_pieces_num = 0

    def to_str(self):
        return vars(self)