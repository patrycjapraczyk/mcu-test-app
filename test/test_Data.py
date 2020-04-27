from unittest import TestCase
from model.Data import Data
from model.GlobalConstants import GlobalConstants


class TestData(TestCase):
    def test_extract_packet_length(self):
        header = 'aa' \
                 '0019' \
                 '00000000' \
                 '00000000' \
                 '00'
        data = Data()
        data.extract_packet_length(header)
        self.assertEqual('0019', data.packet_len)
        self.assertEqual(50, data.len_of_hex)

    def test_extract_message_code(self):
        header = 'aa' \
                 '0019' \
                 '00000000' \
                 '00000000' \
                 '00'
        data = Data()
        data.extract_message_code(header)
        self.assertEqual(GlobalConstants.MESSAGE_CODE_DICT['HEARTBEAT_REQUEST'], data.msg_code)

        header = 'aa' \
                 '0019' \
                 '00000000' \
                 '00000000' \
                 '01'
        data.extract_message_code(header)
        self.assertEqual(GlobalConstants.MESSAGE_CODE_DICT['HEARTBEAT_RESPONSE'], data.msg_code)

        header = 'aa' \
                 '0019' \
                 '00000000' \
                 '00000000' \
                 '02'
        data.extract_message_code(header)
        self.assertEqual(GlobalConstants.MESSAGE_CODE_DICT['RESET_REQUEST'], data.msg_code)

        header = 'aa' \
                 '0019' \
                 '00000000' \
                 '00000000' \
                 '03'
        data.extract_message_code(header)
        self.assertEqual(GlobalConstants.MESSAGE_CODE_DICT['RESET_RESPONSE'], data.msg_code)

        header = 'aa' \
                 '0019' \
                 '00000000' \
                 '00000000' \
                 '04'
        data.extract_message_code(header)
        self.assertEqual(GlobalConstants.MESSAGE_CODE_DICT['ECC_CHECKED'], data.msg_code)

        header = 'aa' \
                 '0019' \
                 '00000000' \
                 '00000000' \
                 '05'
        data.extract_message_code(header)
        self.assertEqual(GlobalConstants.MESSAGE_CODE_DICT['ECC_PERIOD_CHANGE'], data.msg_code)

    def test_extract_data_counter(self):
        header = 'aa' \
                 '0019' \
                 '00000001' \
                 '00000000' \
                 '00'
        data = Data()
        data.extract_data_counter(header)
        self.assertEqual('00000001', data.data_index_hex)
        self.assertEqual(1, data.data_index)
