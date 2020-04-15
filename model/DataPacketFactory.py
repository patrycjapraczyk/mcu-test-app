import binascii
from model.GlobalConstants import GlobalConstants
from model.Calculator import Calculator

class DataPacketFactory:
    MESSAGE_CODE_DICT = {
        'RESET_REQUEST': 0x02
    }

    def get_packet(self, type, data_cnt):
        data = bytearray(b'')
        if type == 'RESET_REQUEST':
            data = self.get_reset_data(data_cnt)

        return data

    def append_len(self, data: bytearray):
        length = len(data)
        data[1] = length >> 8 & 0xff
        data[2] = length & 0xff

    def get_checksum(self, data: bytearray):
        checksum = binascii.crc32(data[GlobalConstants.MSG_CODE_BYTE: len(data) - 1])
        checksum_hex = Calculator.get_hex(checksum, 8)
        return checksum

    def append_checksum(self, data: bytearray):
        checksum = self.get_checksum(data)
        data[GlobalConstants.CHECKSUM_START_BYTE] = checksum >> 24 & 0xff
        data[GlobalConstants.CHECKSUM_START_BYTE] = checksum >> 16 & 0xff
        data[GlobalConstants.CHECKSUM_START_BYTE] = checksum >> 8 & 0xff
        data[GlobalConstants.CHECKSUM_START_BYTE] = checksum & 0xff

    def get_reset_data(self, data_cnt):
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
        data.append(self.MESSAGE_CODE_DICT['RESET_REQUEST'])  # msg_code
        data.append(0x81)  # end_code

        self.append_len(data)
        self.append_checksum(data)
        return data


#data_fact = DataPacketFactory()
#data = data_fact.get_reset_data(0)
#print(data)