import sys, glob, serial, threading, time

from queue import Queue
from model.GlobalConstants import GlobalConstants
from model.DataPacketFactory import DataPacketFactory
from model.ComErrorStorage import ComErrorStorage
from model.Observer.Observer import Observer
from model.Observer.Subject import Subject
from model.Time import Time


class SerialManager(Observer):
    #alter these parameters for your own usecase
    BYTESIZE = 8
    NANOSECONDS_PER_SECOND = 1000000000
    BAUDRATES = [115200, 57600, 19200, 9600]

    def __init__(self, com_error_storage: ComErrorStorage):
        self.com_error_storage = com_error_storage
        self.read_data_queue = Queue()
        self.send_data_queue = Queue()
        self.sent_counter = 0
        self.last_heartbeat_sent = None
        self.last_sent_time = 0
        self.cur_baudrate = 0
        self.heartbeat_period = 1
        self.update_heartbeat_timeout()
        self.lock = threading.Lock()
        self.heartbeat_received = False

    def update(self, subject: Subject) -> None:
        heartbeat_received = subject.heartbeat_received
        if heartbeat_received == self.last_heartbeat:
            cur_time = Time.get_curr_time_ns()
            time_to_period_passed = cur_time - self.last_sent_time
            if time_to_period_passed <= (self.timeout * self.NANOSECONDS_PER_SECOND):
                self.heartbeat_received = True

    def update_heartbeat_timeout(self):
        timeout = self.heartbeat_period * 0.8
        if timeout <= 0.1:
            self.timeout = 0.1
        else:
            self.timeout = timeout

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
                                                 self.BYTESIZE, serial.PARITY_NONE, serial.STOPBITS_ONE)


    def read_data(self):
        """
        reads data coming into the open communication port
        and adds them to te thread-safe queue for data analysis
        """
        data = ''
        while (True):
            self.lock.acquire()
            if not self.serial_port: continue
            new_data = self.serial_port.read()
            self.lock.release()
            if (new_data):
                data += new_data.hex()
                # add the incoming data str to the queue
                if len(data) >= GlobalConstants.MAX_PACKET_LEN:
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

    def send_data(self):
        """
        send a data packet to the open
        serial communication port
        """
        self.send_heartbeat_data()
        time.sleep(self.heartbeat_period)
        while True:
            if not self.heartbeat_received:
                self.com_error_storage.add_error('NO RESPONSE', 0)
            else:
                self.heartbeat_received = False
                self.heartbeat_id += 1

            self.send_heartbeat_data()
            time.sleep(self.heartbeat_period)

    def send_heartbeat_data(self):
        self.lock.acquire()
        #TODO limit the number of data packets that can be sent at one go
        while not self.send_data_queue.empty():
            data = self.send_data_queue.get()
            self.send_data_packet(data)

        heartbeat_packet = DataPacketFactory.get_packet('HEARTBEAT', params={'heartbeat_id': self.heartbeat_id});
        self.last_heartbeat_sent = self.heartbeat_id

        self.send_data_packet(heartbeat_packet)
        self.lock.release()

    def send_data_packet(self, data):
        self.serial_port.write(data)
        self.last_sent_time = Time.get_curr_time_ns()
        self.sent_counter += 1
