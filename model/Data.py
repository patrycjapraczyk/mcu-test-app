from model.Calculator import Calculator


class Data:
    def __init__(self, complete_data="", data_payload="", packet_len="", checksum="", msg_code=""):
        self.complete_data = complete_data
        self.data_payload = data_payload
        self.payload_len = len(data_payload)
        self.packet_len = packet_len
        self.checksum = checksum
        self.msg_code = msg_code
        #number of digits in hexadecimal representation
        if packet_len:
            self.len_of_hex = Calculator.get_int(packet_len) * 2
        else:
            self.len_of_hex = 0

    def to_str(self):
        return str(vars(self))
