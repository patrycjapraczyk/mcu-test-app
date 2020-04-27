from model.GlobalConstants import GlobalConstants
from model.Checksum import Checksum
from model.Calculator import Calculator


class DataPacketFactory:

    def __init__(self):
        self.data_cnt = 0

    @staticmethod
    def get_packet(type, data_cnt, params=[]):
        data = bytearray(b'')
        if type == 'RESET_REQUEST':
            data = DataPacketFactory.get_reset(data_cnt, params)
        elif type == 'HEARTBEAT':
            data = DataPacketFactory.get_heartbeat(data_cnt, params)

        return data

    @staticmethod
    def append_len(data: bytearray):
        length = len(data)
        data[1] = length >> 8 & 0xff
        data[2] = length & 0xff

    @staticmethod
    def append_checksum(data: bytearray):
        checksum = Checksum.crc32(data)
        data[GlobalConstants.CHECKSUM_START_BYTE] = checksum >> 24 & 0xff
        data[GlobalConstants.CHECKSUM_START_BYTE] = checksum >> 16 & 0xff
        data[GlobalConstants.CHECKSUM_START_BYTE] = checksum >> 8 & 0xff
        data[GlobalConstants.CHECKSUM_START_BYTE] = checksum & 0xff

    @staticmethod
    def get_heartbeat(data_cnt, params):
        heartbeat_id = params.heartbeat_id
        if not heartbeat_id:
            return None

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
        DataPacketFactory.append_data(Calculator.get_bytearray(heartbeat_id))
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
    def append_data(data: bytearray, data_content: bytearray):
        for (i, data_byte) in enumerate(data_content):
            data.append(bytes[i]) #data index
            data.append(data_byte) #data piece

