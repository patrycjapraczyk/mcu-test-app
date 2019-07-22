from Calculator import Calculator


class Data:
    def __init__(self, data_payload="", buff_len=""):
        self.data_payload = data_payload
        self.payload_len = len(data_payload)
        self.buff_len = buff_len
        if buff_len:
            self.len_of_hex = Calculator.get_int(buff_len) * 2
        else:
            self.len_of_hex = 0

    def to_str(self):
        return str(vars(self))
