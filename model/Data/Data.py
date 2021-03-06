from model.StaticClasses.Calculator import Calculator
from model.StaticClasses.GlobalConstants import GlobalConstants
from model.StaticClasses.StrManipulator import StrManipulator
from model.StaticClasses.DataStructFunctions import DataStructFunctions


class Data:
    def __init__(self, complete_data=''):
        self.time = ''
        self.complete_data = complete_data
        self.data_payload = ''
        self.payload_len = 0
        self.packet_len = ''
        self.checksum = ''
        self.msg_code = ''
        self.data_index = 0
        self.data_index_hex = ''
        self.len_of_hex = 0 #number of digits in hexadecimal representation
        self.purpose = ''
        self.data_payload_value = ''

        if self.complete_data:
            header = StrManipulator.substring(self.complete_data, 0, GlobalConstants.DATA_PAYLOAD_START_INDEX)
            payload = StrManipulator.substring(self.complete_data, GlobalConstants.DATA_PAYLOAD_START_INDEX, len(self.complete_data))
            self.add_header_info(header)
            self.data_payload = payload

    def to_str(self):
        return str(vars(self))

    def add_header_info(self, data_header: str):
        self.complete_data += data_header
        self.extract_packet_length(data_header)
        self.extract_data_counter(data_header)
        self.extract_message_code(data_header)
        self.extract_checksum(data_header)

    def extract_packet_length(self, data_header: str):
        self.packet_len = StrManipulator.substring(data_header, GlobalConstants.PACKET_LEN_START_INDEX,
                                                   GlobalConstants.PACKET_LEN_END_INDEX)
        int_len = Calculator.get_int(self.packet_len)
        # number of hex digits
        self.len_of_hex = int_len * 2

    def extract_message_code(self, data_header: str):
        msg_code = StrManipulator.substring(data_header, GlobalConstants.MSG_CODE_START_INDEX,
                                            GlobalConstants.MSG_CODE_END_INDEX)
        msg_code = Calculator.get_int(msg_code)
        self.msg_code = msg_code
        self.purpose = DataStructFunctions.get_key(GlobalConstants.MESSAGE_CODE_DICT, msg_code)

    def extract_data_counter(self, data_header: str):
        data_index = StrManipulator.substring(data_header, GlobalConstants.DATA_COUNTER_START_INDEX,
                                              GlobalConstants.DATA_COUNTER_END_INDEX)
        self.data_index = Calculator.get_int(data_index)
        self.data_index_hex = data_index

    def extract_checksum(self, data_header: str):
        checksum = StrManipulator.substring(data_header, GlobalConstants.CHECKSUM_START_INDEX,
                                            GlobalConstants.CHECKSUM_END_INDEX)
        self.checksum = Calculator.get_int(checksum)

    def extract_data_payload(self):
        # remove indices
        if not self.data_payload_value:
            payload = StrManipulator.split_string(self.data_payload, GlobalConstants.PAYLOAD_INDICES_LEN)
            payload = StrManipulator.remove_every_other(payload, True)
            payload = StrManipulator.list_into_str(payload)
            self.data_payload_value = payload
