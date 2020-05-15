import sys, glob, serial, threading, time

from queue import Queue
from model.GlobalConstants import GlobalConstants
from model.DataPacketFactory import DataPacketFactory
from model.ComErrorStorage import ComErrorStorage
from model.ComError import ComError
from model.Observer.Observer import Observer
from model.Observer.Subject import Subject
from model.Time import Time
from model.Calculator import Calculator


class SerialManager(Observer):
    #alter these parameters for your own usecase
    BYTESIZE = 8
    NANOSECONDS_PER_MILI_SECOND = 1000000
    BAUDRATES = [115200, 57600, 19200, 9600]
    HEARTBEAT_PERIODS_ALL = [100, 250, 500, 1000]
    HEARTBEAT_PERIODS_MEDIUM = [250, 500, 1000]
    HEARTBEAT_PERIODS_UPPER = [500, 1000]

    def __init__(self, com_error_storage: ComErrorStorage):
        self.__stopped = False
        self.com_error_storage = com_error_storage
        self.read_data_queue = Queue()
        self.send_data_queue = Queue()
        self.sent_counter = 0
        self.last_heartbeat_sent_id = ''
        self.last_sent_time = 0
        self.cur_baudrate = 0

        self.heartbeat_id = 0
        self.heartbeat_period_rates = self.HEARTBEAT_PERIODS_ALL

        self.curr_heartbeat_period = 1000
        self.cur_ecc_period = 1000

        self.update_heartbeat_timeout()

        self.serial_port = None
        self.heartbeat_received = False

    def update(self, subject: Subject) -> None:
        heartbeat_received = subject.heartbeat_received_id
        if heartbeat_received != '' and heartbeat_received == self.last_heartbeat_sent_id:
            self.heartbeat_received = True
            curr_time = Time.get_curr_time()
            print(str(curr_time) + ' heartbeats matching, heartbeat received: ' + str(heartbeat_received))

    def update_heartbeat_timeout(self):
        # timeout = self.curr_heartbeat_period * 0.8
        # if timeout <= 0.1:
        #     self.timeout = 0.1
        # else:
        #     self.timeout = timeout
        self.timeout = self.curr_heartbeat_period

    @staticmethod
    def serial_ports():
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    @staticmethod
    def baudrates():
        """
        :return: returns a list of convenient baudrate values
        """
        return SerialManager.BAUDRATES

    def init_connection(self, port, baudrate: int):
        """
        opens a serial communication port
        """
        if baudrate in self.BAUDRATES and port in self.serial_ports():
            self.cur_baudrate = baudrate
            self.serial_port = serial.Serial(port, baudrate,
                                                 self.BYTESIZE, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=0)
            self.adjust_curr_heartbeat_rate()

    def read_data(self):
        """
        reads data coming into the open communication port
        and adds them to te thread-safe queue for data analysis
        """
        data = ''
        while not self.has_timeout_passed():
            if not self.serial_port: continue
            new_data = self.serial_port.read()
            if new_data:
                data += new_data.hex()
                # add the incoming data str to the queue
                if len(data) >= GlobalConstants.HEARTBEAT_RESPONSE_LEN:
                    self.read_data_queue.put(data)
                    curr_time = Time.get_curr_time()
                    print(str(curr_time) + ' read data: ' + data)
                    data = ''

        if data != '':
            self.read_data_queue.put(data)
            curr_time = Time.get_curr_time()
            print(str(curr_time) + ' read data: ' + data)

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
            self.com_error_storage.add_error(err, 0)
        else:
            self.heartbeat_received = False

            if self.heartbeat_id >= GlobalConstants.HEARTBEAT_ID_MAX:
                self.heartbeat_id = 0
            else:
                self.heartbeat_id += 1

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

    def send_heartbeat_data(self):
        #TODO limit the number of data packets that can be sent at one go
        while not self.send_data_queue.empty():
            data = self.send_data_queue.get()
            self.send_data_packet(data)

        curr_heartbeat_period_id = GlobalConstants.HEARTBEAT_PERIODS[self.curr_heartbeat_period]
        heartbeat_packet = DataPacketFactory.get_packet('HEARTBEAT', self.sent_counter,
                                                        params={'heartbeat_id': self.heartbeat_id,
                                                                'heartbeat_period': curr_heartbeat_period_id})

        self.last_heartbeat_sent_id = self.heartbeat_id
        self.send_data_packet(heartbeat_packet)

    def send_data_packet(self, data: bytearray):
        if not self.serial_port:
            return False
        data_str = Calculator.get_hex_str(data)
        curr_time = Time.get_curr_time()
        print(str(curr_time) + ' sent data: ' + data_str)
        self.serial_port.write(data)
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
        ecc_period_change_packet = DataPacketFactory.get_packet('ECC_PERIOD_CHANGE', self.sent_counter,
                                     params={'period_id': period_id})
        self.add_data_to_send_queue(ecc_period_change_packet)




