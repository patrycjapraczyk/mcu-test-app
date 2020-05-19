import serial, time

from model.DataPacketFactory import DataPacketFactory
from model.GlobalConstants import GlobalConstants
from model.StrManipulator import StrManipulator
from model.Calculator import Calculator
from queue import Queue
from model.Data import Data
from model.SerialManager import SerialManager
from model.DataStructFunctions import DataStructFunctions
from threading import Thread


class TestSerialCom:
    COM_PORT_NAME = 'COM1'
    BAUDRATE = 9600
    BYTESIZE = 8
    PACKET_LEN = 253

    def __init__(self):
        self.data_cnt = 0
        self.curr_heartbeat_period = 1000
        self.cur_ecc_period = 1000
        self.send_data_queue = Queue()
        self.read_data_queue = Queue()
        self.new_data_to_read = True


    def init_com(self):
        """
        opens a serial communication port
        """
        self.serial_port = serial.Serial(self.COM_PORT_NAME, self.BAUDRATE,
                                        self.BYTESIZE, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=0)

    def send_data_packet(self, data):
        """
        send a generated data packet to the connected
        serial communication port
        """
        self.serial_port.write(data)
        self.data_cnt += 1

    def generate_ecc_check(self):
        ecc_check_frame = 'aa002000000000168d0499040000ffff00010000000201a40003000000040081'
        byte_len = int(len(ecc_check_frame)/2)
        ecc_check_frame = Calculator.get_int(ecc_check_frame)
        ecc_check_frame = Calculator.get_bytearray(ecc_check_frame, byte_len)
        while True :
            self.send_data_queue.put(ecc_check_frame)
            time.sleep(self.cur_ecc_period/1000)

    def read_data(self):
        """
        reads data coming into the open communication port
        and adds them to te thread-safe queue for data analysis
        """
        while True:
            if not self.serial_port: continue
            new_data = self.serial_port.read()
            new_data = new_data.hex()
            self.read_data_queue.put(new_data)

    def analyse_data(self):
        data = ''
        expected_data_len = GlobalConstants.HEX_DIGITS_PER_BYTE * GlobalConstants.MAX_PACKET_LEN + 1
        data_len_hex = ''
        while True:
            if not self.serial_port: continue
            new_data = self.read_data_queue.get()
            if new_data:
                if self.new_data_to_read:
                    if new_data == GlobalConstants.START_CODE:
                        data += new_data
                        self.new_data_to_read = False
                else:
                    if len(data) < expected_data_len:
                        data += new_data
                        # extract
                        if GlobalConstants.PACKET_LEN_START_INDEX <= len(data) <= GlobalConstants.PACKET_LEN_END_INDEX:
                            data_len_hex += new_data
                        if len(data) == GlobalConstants.DATA_COUNTER_END_INDEX:
                            expected_data_len = Calculator.get_int(data_len_hex) * GlobalConstants.HEX_DIGITS_PER_BYTE
                        if len(data) == expected_data_len:
                            data_packet = Data(data)
                            self.analyse_data_purpose(data_packet)
                            # clear data
                            self.new_data_to_read = True
                            data = ''
                            expected_data_len = GlobalConstants.HEX_DIGITS_PER_BYTE * GlobalConstants.MAX_PACKET_LEN + 1
                            data_len_hex = ''

    def analyse_data_purpose(self, data_packet: Data):
        data_payload = data_packet.data_payload
        if data_packet.purpose == 'HEARTBEAT_REQUEST':
            heartbeat = self.analyse_heartbeat(data_payload)
            self.send_data_stream(heartbeat)

    def analyse_heartbeat(self, data_payload: str):
        period = StrManipulator.substring(data_payload, GlobalConstants.HEARTBEAT_PERIOD_START, GlobalConstants.HEARTBEAT_PERIOD_END)
        period = Calculator.get_int(period)
        self.curr_heartbeat_period = DataStructFunctions.get_key(GlobalConstants.HEARTBEAT_PERIODS, period)
        id = StrManipulator.substring(data_payload, GlobalConstants.HEARTBEAT_ID_START, GlobalConstants.HEARTBEAT_ID_END)
        id = Calculator.get_int(id)
        heartbeat = DataPacketFactory.get_heartbeat_response(self.data_cnt, {'heartbeat_id': id})
        return heartbeat

    def send_data_stream(self, heartbeat: bytearray):
        data_sent = 0
        max_frames = SerialManager.get_max_frames_num(self.curr_heartbeat_period, TestSerialCom.BAUDRATE)
        while (not self.send_data_queue.empty()) and data_sent < max_frames:
            data = self.send_data_queue.get()
            self.send_data_packet(data)
            data_sent += 1

        self.send_data_packet(heartbeat)


test = TestSerialCom()
test.init_com()

ecc_check_thread = Thread(target=test.generate_ecc_check)
ecc_check_thread.start()

read_data_thread = Thread(target=test.read_data)
read_data_thread.start()

analyse_data_thread = Thread(target=test.analyse_data)
analyse_data_thread.start()
