import serial
import time

from model.DataPacketFactory import DataPacketFactory
from model.GlobalConstants import GlobalConstants
from model.StrManipulator import StrManipulator
from model.Calculator import Calculator


class TestSerialCom:
    COM_PORT_NAME = 'COM1'
    BAUDRATE = 9600
    BYTESIZE = 8
    PACKET_LEN = 253

    def __init__(self):
        self.data_cnt = 0

    def init_com(self):
        """
        opens a serial communication port
        """
        self.serial_port = serial.Serial(self.COM_PORT_NAME, self.BAUDRATE,
                                        self.BYTESIZE, serial.PARITY_NONE, serial.STOPBITS_ONE)


    def send_data_packet(self, data):
        """
        send a generated data packet to the connected
        serial communication port
        """

        self.serial_port.write(data)

    def read_data_packets(self):
        """
        Constantly sends a generated data packet for every period value
        to the connected serial communication port
        :param period: time in s
        :return:
        """
        data = ''
        while True:
            if not self.serial_port: continue
            new_data = self.serial_port.read()
            print(new_data)
            if new_data:
                data += new_data.hex()
                # add the incoming data str to the queue
                if len(data) >= GlobalConstants.HEARTBEAT_LEN * GlobalConstants.HEX_DIGITS_PER_BYTE + 2:
                    new_data = data[GlobalConstants.DATA_PAYLOAD_START_INDEX:]
                    index_list = StrManipulator.split_string(new_data, GlobalConstants.PAYLOAD_INDICES_LEN)
                    index_list = StrManipulator.remove_every_other(index_list, True)
                    new_data = StrManipulator.list_into_str(index_list)
                    heartbeat_id = StrManipulator.substring(new_data, GlobalConstants.HEARTBEAT_ID_START, GlobalConstants.HEARTBEAT_ID_END)
                    heartbeat_id = Calculator.get_int(heartbeat_id)
                    params = {'heartbeat_id': heartbeat_id}
                    heartbeat_response = DataPacketFactory.get_packet('HEARTBEAT_RESPONSE', 0, params)
                    self.send_data_packet(heartbeat_response)
                    print('SENT VALS')


test = TestSerialCom()
test.init_com()
test.read_data_packets()