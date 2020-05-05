from model.GlobalConstants import GlobalConstants
from model.Checksum import Checksum
from model.Calculator import Calculator
from model.ListFunctions import ListFunctions


class DataPacketFactory:

    def __init__(self):
        self.data_cnt = 0

    @staticmethod
    def get_packet(type, data_cnt, params=[]):
        data = bytearray(b'')
        if type == 'RESET_REQUEST':
            data = DataPacketFactory.get_reset(data_cnt, params)
        elif type == 'HEARTBEAT':
            data = DataPacketFactory.get_heartbeat_request(data_cnt, params)
        elif type == 'HEARTBEAT_RESPONSE':
            data = DataPacketFactory.get_heartbeat_response(data_cnt, params)
        elif type == 'ECC_PERIOD_CHANGE':
            data = DataPacketFactory.get_ecc_period_change(data_cnt, params)
        return data

    @staticmethod
    def append_len(data: bytearray):
        length = len(data)
        data[1] = length >> 8 & 0xff
        data[2] = length & 0xff

    @staticmethod
    def append_checksum(data: bytearray):
        checksum = Checksum.crc32(data[GlobalConstants.MSG_CODE_BYTE: len(data) - 1])
        data[GlobalConstants.CHECKSUM_START_BYTE] = checksum >> 24 & 0xff
        data[GlobalConstants.CHECKSUM_START_BYTE + 1] = checksum >> 16 & 0xff
        data[GlobalConstants.CHECKSUM_START_BYTE + 2] = checksum >> 8 & 0xff
        data[GlobalConstants.CHECKSUM_START_BYTE + 3] = checksum & 0xff

    @staticmethod
    def get_heartbeat_request(data_cnt, params):
        heartbeat_id = params['heartbeat_id']
        curr_heartbeat_period = params['heartbeat_period']
        data = bytearray(b'')

        data.append(0xaa)  # start code
        data.append(0)  # packet len[0]
        data.append(0)  # packet len[1]
        data.append(data_cnt >> 24 & 0xff)  # data_cnt[0]
        data.append(data_cnt >> 16 & 0xff)  # data_cnt[1]
        data.append(data_cnt >> 8 & 0xff)  # data_cnt[2]
        data.append(data_cnt & 0xff)  # data_cnt[3]
        data.append(0)  # checksum[0]
        data.append(0)  # checksum[1]
        data.append(0)  # checksum[2]
        data.append(0)  # checksum[3]
        data.append(GlobalConstants.MESSAGE_CODE_DICT['HEARTBEAT_REQUEST'])  # msg_code
        data_content = Calculator.get_bytearray(curr_heartbeat_period, 1) + Calculator.get_bytearray(heartbeat_id, 4)
        DataPacketFactory.append_data(data, data_content)
        data.append(0x81)  # end_code

        DataPacketFactory.append_len(data)
        DataPacketFactory.append_checksum(data)
        return data

    @staticmethod
    def get_heartbeat_response(data_cnt, params):
        heartbeat_id = params['heartbeat_id']
        data = bytearray(b'')
        data.append(0xaa)  # start code
        data.append(0)  # packet len[0]
        data.append(0)  # packet len[1]
        data.append(data_cnt >> 24 & 0xff)  # data_cnt[0]
        data.append(data_cnt >> 16 & 0xff)  # data_cnt[1]
        data.append(data_cnt >> 8 & 0xff)  # data_cnt[2]
        data.append(data_cnt & 0xff)  # data_cnt[3]
        data.append(0)  # checksum[0]
        data.append(0)  # checksum[1]
        data.append(0)  # checksum[2]
        data.append(0)  # checksum[3]
        data.append(GlobalConstants.MESSAGE_CODE_DICT['HEARTBEAT_RESPONSE'])  # msg_code
        DataPacketFactory.append_data(data, Calculator.get_bytearray(heartbeat_id))
        data.append(0x81)  # end_code

        DataPacketFactory.append_len(data)
        DataPacketFactory.append_checksum(data)
        return data

    @staticmethod
    def get_reset(data_cnt, params=[]):
        data = bytearray(b'')
        data.append(0xaa)  # start code
        data.append(0)  # packet len[0]
        data.append(0)  # packet len[1]
        data.append(data_cnt >> 24 & 0xff)  # data_cnt[0]
        data.append(data_cnt >> 16 & 0xff)  # data_cnt[1]
        data.append(data_cnt >> 8 & 0xff)  # data_cnt[2]
        data.append(data_cnt & 0xff)  # data_cnt[3]
        data.append(0)  # checksum[0]
        data.append(0)  # checksum[1]
        data.append(0)  # checksum[2]
        data.append(0)  # checksum[3]
        data.append(GlobalConstants.MESSAGE_CODE_DICT['RESET_REQUEST'])  # msg_code
        data.append(0x81)  # end_code

        DataPacketFactory.append_len(data)
        DataPacketFactory.append_checksum(data)
        return data

    @staticmethod
    def get_ecc_period_change(data_cnt, params=[]):
        period_id = params['period_id']
        data = bytearray(b'')
        data.append(0xaa)  # start code
        data.append(0)  # packet len[0]
        data.append(0)  # packet len[1]
        data.append(data_cnt >> 24 & 0xff)  # data_cnt[0]
        data.append(data_cnt >> 16 & 0xff)  # data_cnt[1]
        data.append(data_cnt >> 8 & 0xff)  # data_cnt[2]
        data.append(data_cnt & 0xff)  # data_cnt[3]
        data.append(0)  # checksum[0]
        data.append(0)  # checksum[1]
        data.append(0)  # checksum[2]
        data.append(0)  # checksum[3]
        data.append(GlobalConstants.MESSAGE_CODE_DICT['ECC_PERIOD_CHANGE'])  # msg_code
        DataPacketFactory.append_data(data, Calculator.get_bytearray(period_id, bytelen=1))
        data.append(0x81)  # end_code

        DataPacketFactory.append_len(data)
        DataPacketFactory.append_checksum(data)
        return data

    @staticmethod
    def append_data(data: bytearray, data_content: bytearray):
        data_content_paired = list(ListFunctions.chunk(data_content, 2))
        num_seq = range(0, len(data_content_paired))
        num_seq = list(map(lambda x: Calculator.get_bytearray(x, bytelen=2), num_seq))

        i = 0
        while i < len(num_seq):
            cur_index = num_seq[i]
            cur_data = data_content_paired[i]
            data += cur_index
            data += cur_data
            i += 1
