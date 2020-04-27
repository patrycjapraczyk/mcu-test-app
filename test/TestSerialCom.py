import serial
import time

from model.GlobalConstants import GlobalConstants

class TestSerialCom:
    COM_PORT_NAME = 'COM2'
    BAUDRATE = 9600
    BYTESIZE = 8
    PACKET_LEN = 253

    def __init__(self):
        self.data_cnt = 0
        self.populate_data()
        self.curr_data = 0

    def init_com(self):
        """
        opens a serial communication port
        """
        self.serial_port = serial.Serial(self.COM_PORT_NAME, self.BAUDRATE,
                                        self.BYTESIZE, serial.PARITY_NONE, serial.STOPBITS_ONE)

    def populate_data(self):
        """
        populates data with consecutive numbers
        """
        MAX_DATA_VAL = 256
        self.data = list(range(0, MAX_DATA_VAL))

    def generate_packet(self) -> bytearray:
        """
        generates a data packet based on the established protocol
        fills in data packet with the current value from self.data
        :return: data packet as a byte_array
        """
        data = bytearray(b'')
        data.append(0xaa) #start code
        data.append(self.PACKET_LEN >> 8 & 0xff) #packet len[0]
        data.append(self.PACKET_LEN & 0xff) #packet len[1]
        data.append(self.data_cnt >> 24 & 0xff) #data_cnt[0]
        data.append(self.data_cnt >> 16 & 0xff) #data_cnt[1]
        data.append(self.data_cnt >> 8 & 0xff) #data_cnt[2]
        data.append(self.data_cnt & 0xff) #data_cnt[3]
        data.append(0) #checksum[0]
        data.append(0) #checksum[1]
        data.append(0) #checksum[2]
        data.append(0) #checksum[3]
        data.append(0) #msg_code

        i = 0
        while(len(data) < GlobalConstants.MAX_PACKET_LEN - 1 - 4):
            data.append(i >> 8 & 0xff)  # index[0]
            data.append(i & 0xff)  # index[1]
            data.append(self.curr_data >> 8  & 0xff)  # msg_code[0]
            data.append(self.curr_data  & 0xff)  # msg_code[1]

            i = i + 1
            self.curr_data += 1

        data.append(0x81)

        self.data_cnt += 1

        return data

    def send_data_packet(self):
        """
        send a generated data packet to the connected
        serial communication port
        """
        data_arr = self.generate_packet()
        data = bytes(data_arr)
        self.serial_port.write(data)

    def send_data_packets(self, period):
        """
        Constantly sends a generated data packet for every period value
        to the connected serial communication port
        :param period: time in s
        :return:
        """
        while(True):
            self.send_data_packet()
            time.sleep(period)


test = TestSerialCom()
test.init_com()
test.send_data_packets(2)