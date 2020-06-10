import sys, glob, serial, math

from queue import Queue

from model.StaticClasses.GlobalConstants import GlobalConstants
from model.StaticClasses.DataPacketFactory import DataPacketFactory
from model.Data.ComErrorStorage import ComErrorStorage
from model.Data.ComError import ComError
from model.Observer.Observer import Observer
from model.Observer.Subject import Subject
from model.StaticClasses.Time import Time
from model.StaticClasses.Calculator import Calculator
from model.Interfaces import ComInterface
from model.Communication.ComInterfaceFactory import ComInterfaceFactory
from model.Communication.SerialManager import SerialManager


class CommunicationManager(Observer):
    NANOSECONDS_PER_MILI_SECOND = 1000000
    BAUDRATES = [115200, 57600, 19200, 9600]
    HEARTBEAT_PERIODS_ALL = [100, 250, 500, 1000]
    HEARTBEAT_PERIODS_MEDIUM = [250, 500, 1000]
    HEARTBEAT_PERIODS_UPPER = [500, 1000]
    INTERFACE_TYPE = 'SERIAL'

    def __init__(self, com_error_storage: ComErrorStorage):
        self.__stopped = False
        self.com_error_storage = com_error_storage
        self.read_data_queue = Queue()
        self.send_data_queue = Queue()
        self.sent_counter = 0
        self.last_heartbeat_sent_id = ''
        self.last_sent_time = 0

        self.cur_heartbeat_id = 0
        self.heartbeat_period_rates = self.HEARTBEAT_PERIODS_ALL

        self.cur_baudrate = 0
        self.curr_heartbeat_period = 1000
        self.cur_ecc_period = 1000

        self.update_heartbeat_timeout()

        self.com_interface = ComInterfaceFactory.get_interface(self.INTERFACE_TYPE)

        self.heartbeat_received = False

    def update(self, subject: Subject) -> None:
        """
        :param subject: in this case DataProcessingThread class
        """
        heartbeat_received = subject.heartbeat_received_id
        if heartbeat_received != '' and heartbeat_received == self.last_heartbeat_sent_id:
            self.heartbeat_received = True
            curr_time = Time.get_curr_time()
            print(str(curr_time) + ' heartbeats matching, heartbeat received: ' + str(heartbeat_received))

    def update_heartbeat_timeout(self):
        self.timeout = self.curr_heartbeat_period

    @staticmethod
    def baudrates():
        """
        :return: returns a list of convenient baudrate values
        """
        return CommunicationManager.BAUDRATES

    def init_connection(self, port, baudrate: int):
        if baudrate in self.BAUDRATES and port in SerialManager.serial_ports():
            self.cur_baudrate = baudrate
            self.com_interface.init_connection(port, baudrate)
            self.adjust_curr_heartbeat_rate()

    def read_data(self):
        """
        reads data coming into the open communication port
        and adds them to te thread-safe queue for data analysis
        """
        data = ''
        while not self.has_timeout_passed():
            if not self.com_interface.is_connected(): continue
            new_data = self.com_interface.read_data()
            if new_data:
                data += new_data.hex()
                # add the incoming data str to the queue
                self.read_data_queue.put(data)
                data = ''

    def add_data_to_send_queue(self, data: bytearray):
        """
        @requires data packet is in agreement with the protocol specified
        and is a bytearray
        puts data into a queue to be send
        :param data: bytearray - data to be sent
        :return:
        """
        self.send_data_queue.put(data)

    def check_heartbeat_received(self):
        if not self.heartbeat_received:
            err = ComError('NO RESPONSE', '')
            self.com_error_storage.add(err, 0)
        else:
            self.heartbeat_received = False

            if self.cur_heartbeat_id >= GlobalConstants.HEARTBEAT_ID_MAX:
                self.cur_heartbeat_id = 0
            else:
                self.cur_heartbeat_id += 1

    def heartbeat_loop(self):
        while self.__stopped is False:
            self.send_heartbeat_data()
            self.read_data()
            self.check_heartbeat_received()

    def stop(self):
        self.__stopped = True

    def has_timeout_passed(self):
        cur_time = Time.get_curr_time_ns()
        time_passed = cur_time - self.last_sent_time
        if time_passed < (self.timeout * self.NANOSECONDS_PER_MILI_SECOND):
            return False
        return True

    @staticmethod
    def get_max_frames_num(hb_period, baudrate):
        max = math.floor((hb_period/1000 * baudrate / (GlobalConstants.SERIAL_BYTE_LEN * GlobalConstants.MAX_PACKET_LEN) -
                          GlobalConstants.HEARTBEAT_LEN / GlobalConstants.MAX_PACKET_LEN))
        return max

    def send_heartbeat_data(self):
        data_sent = 0
        max_frames = CommunicationManager.get_max_frames_num(self.curr_heartbeat_period, self.cur_baudrate)
        while not self.send_data_queue.empty() and data_sent < max_frames:
            data = self.send_data_queue.get()
            self.send_data_packet(data)
            print(data)
            data_sent += 1

        curr_heartbeat_period_id = GlobalConstants.HEARTBEAT_PERIODS[self.curr_heartbeat_period]
        heartbeat_packet = DataPacketFactory.get_packet('HEARTBEAT',
                                                        params={'heartbeat_id': self.cur_heartbeat_id,
                                                                'heartbeat_period': curr_heartbeat_period_id})
        self.last_heartbeat_sent_id = self.cur_heartbeat_id
        self.send_data_packet(heartbeat_packet)

    def send_data_packet(self, data: bytearray):
        if not self.com_interface.is_connected():
            return False
        data_str = Calculator.get_hex_str(data)
        curr_time = Time.get_curr_time()
        print(str(curr_time) + ' sent data: ' + data_str)
        DataPacketFactory.adjust_data_cnt(data, self.sent_counter)
        self.com_interface.send_data(data)
        self.last_sent_time = Time.get_curr_time_ns()

        if self.sent_counter >= GlobalConstants.DATA_INDEX_MAX:
            self.sent_counter = 0
        else:
            self.sent_counter += 1
        return True

    def adjust_curr_heartbeat_rate(self):
        if self.cur_baudrate == 9600:
            self.heartbeat_period_rates = self.HEARTBEAT_PERIODS_UPPER
        elif self.cur_baudrate == 19200:
            self.heartbeat_period_rates = self.HEARTBEAT_PERIODS_MEDIUM

    def set_heartbeat_period(self, heartbeat_period):
        if heartbeat_period in GlobalConstants.HEARTBEAT_PERIODS.keys():
            self.curr_heartbeat_period = heartbeat_period
            self.update_heartbeat_timeout()
            return True
        return False

    def set_ecc_period(self, ecc_period):
        if ecc_period in GlobalConstants.ECC_CHECK_PERIODS.keys():
            ecc_period_id = GlobalConstants.ECC_CHECK_PERIODS[ecc_period]
            if ecc_period != self.cur_ecc_period:
                self.cur_ecc_period = ecc_period
                self.send_ecc_period_change(ecc_period_id)
                return True
        return False

    def send_ecc_period_change(self, period_id):
        ecc_period_change_packet = DataPacketFactory.get_packet('ECC_PERIOD_CHANGE',
                                                                params={'period_id': period_id})
        self.add_data_to_send_queue(ecc_period_change_packet)
