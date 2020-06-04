from model.StaticClasses.GlobalConstants import GlobalConstants
from model.StaticClasses.Checksum import Checksum
from model.StaticClasses.Calculator import Calculator
from model.StaticClasses.DataStructFunctions import DataStructFunctions


class DataPacketFactory:

    @staticmethod
    def get_packet(type: str, params: object = {}) -> bytearray:
        data = bytearray(b'')
        if type == 'RESET_REQUEST':
            data = DataPacketFactory.get_reset(params)
        elif type == 'RESET_RESPONSE':
            data = DataPacketFactory.get_reset_response(params)
        elif type == 'HEARTBEAT':
            data = DataPacketFactory.get_heartbeat_request(params)
        elif type == 'HEARTBEAT_RESPONSE':
            data = DataPacketFactory.get_heartbeat_response(params)
        elif type == 'ECC_PERIOD_CHANGE':
            data = DataPacketFactory.get_ecc_period_change(params)
        elif type == 'ECC_CHECKED':
            data = DataPacketFactory.get_ecc_check(params)
        return data

    @staticmethod
    def adjust_data_cnt(data: bytearray, data_cnt: int):
        data[3] = data_cnt >> 24 & 0xff
        data[4] = data_cnt >> 16 & 0xff
        data[5] = data_cnt >> 8 & 0xff
        data[6] = data_cnt & 0xff

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
    def get_heartbeat_request(params):
        heartbeat_id = params['heartbeat_id']
        curr_heartbeat_period = params['heartbeat_period']
        data = DataPacketFactory.init_packet()
        data.append(GlobalConstants.MESSAGE_CODE_DICT['HEARTBEAT_REQUEST'])  # msg_code
        data_content = Calculator.get_bytearray(curr_heartbeat_period, 1) + Calculator.get_bytearray(heartbeat_id, 4)
        DataPacketFactory.append_data(data, data_content)
        data.append(0x81)  # end_code

        DataPacketFactory.append_len(data)
        DataPacketFactory.append_checksum(data)
        return data

    @staticmethod
    def get_heartbeat_response(params):
        heartbeat_id = params['heartbeat_id']
        data = DataPacketFactory.init_packet()
        data.append(GlobalConstants.MESSAGE_CODE_DICT['HEARTBEAT_RESPONSE'])  # msg_code
        DataPacketFactory.append_data(data, Calculator.get_bytearray(heartbeat_id, 4))
        data.append(0x81)  # end_code

        DataPacketFactory.append_len(data)
        DataPacketFactory.append_checksum(data)
        return data

    @staticmethod
    def get_reset(params=[]):
        data = DataPacketFactory.init_packet()
        data.append(GlobalConstants.MESSAGE_CODE_DICT['RESET_REQUEST'])  # msg_code
        data.append(0x81)  # end_code

        DataPacketFactory.append_len(data)
        DataPacketFactory.append_checksum(data)
        return data

    @staticmethod
    def get_reset_response(params):
        data = DataPacketFactory.init_packet()
        data.append(GlobalConstants.MESSAGE_CODE_DICT['RESET_RESPONSE']) #msg_code
        reset_reason = params['reset_reason']
        reset_reason = Calculator.get_bytearray(reset_reason, 1)
        DataPacketFactory.append_data(data, reset_reason)
        data.append(0x81)

        DataPacketFactory.append_len(data)
        DataPacketFactory.append_checksum(data)
        return data

    @staticmethod
    def get_ecc_check(params=[]):
        index = params['index']
        err_cnt = params['err_cnt']
        overflow = params['overflow']
        ecc_addresses_str = params['ecc_addresses']
        ecc_addresses = Calculator.get_int(ecc_addresses_str)

        data = DataPacketFactory.init_packet()
        data.append(GlobalConstants.MESSAGE_CODE_DICT['ECC_CHECKED'])  # msg_code

        data_content = Calculator.get_bytearray(index, bytelen=2)
        data_content += Calculator.get_bytearray(err_cnt, bytelen=3)
        overflow_byte = 0 if overflow else 1
        data_content += Calculator.get_bytearray(overflow_byte, bytelen=1)
        data_content += Calculator.get_bytearray(ecc_addresses, bytelen=int(len(ecc_addresses_str)/2))

        DataPacketFactory.append_data(data, data_content)
        data.append(0x81)  # end_code

        DataPacketFactory.append_len(data)
        DataPacketFactory.append_checksum(data)
        return data

    @staticmethod
    def get_ecc_period_change(params=[]):
        period_id = params['period_id']
        data = DataPacketFactory.init_packet()
        data.append(GlobalConstants.MESSAGE_CODE_DICT['ECC_PERIOD_CHANGE'])  # msg_code
        DataPacketFactory.append_data(data, Calculator.get_bytearray(period_id, bytelen=1))
        data.append(0x81)  # end_code

        DataPacketFactory.append_len(data)
        DataPacketFactory.append_checksum(data)
        return data

    @staticmethod
    def init_packet():
        data = bytearray(b'')
        data.append(0xaa)  # start code
        data.append(0)  # packet len[0]
        data.append(0)  # packet len[1]
        data.append(0)  # data_cnt[0]
        data.append(0)  # data_cnt[1]
        data.append(0)  # data_cnt[2]
        data.append(0)  # data_cnt[3]
        data.append(0)  # checksum[0]
        data.append(0)  # checksum[1]
        data.append(0)  # checksum[2]
        data.append(0)  # checksum[3]
        return data

    @staticmethod
    def append_data(data: bytearray, data_content: bytearray):
        data_content_paired = list(DataStructFunctions.chunk(data_content, 2))
        num_seq = range(0, len(data_content_paired))
        num_seq = list(map(lambda x: Calculator.get_bytearray(x, bytelen=2), num_seq))

        i = 0
        while i < len(num_seq):
            cur_index = num_seq[i]
            cur_data = data_content_paired[i]
            data += cur_index
            data += cur_data
            i += 1
