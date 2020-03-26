import sys
import glob
import serial

from queue import Queue
from DataProcessingThread import DataProcessingThread
from GlobalConstants import GlobalConstants


class SerialManager:
    #alter these parameters for your own usecase
    COM_PORT_NAME = 'COM1'
    BAUDRATE = 9600
    BYTESIZE = 8

    def __init__(self):
        self.q = Queue()
        self.start_data_processing_thread()

    def serial_ports(self):
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

    def print_ports(self):
        print(self.serial_ports())

    def init_connection(self):
        """
        opens a serial communication port
        """
        self.serialPort = serial.Serial(self.COM_PORT_NAME, self.BAUDRATE,
                                        self.BYTESIZE, serial.PARITY_NONE, serial.STOPBITS_ONE)

    def start_data_processing_thread(self):
        """
        creates and starts data analysis thread
        """
        # pass the data to the thread via the queue
        t = DataProcessingThread(self.q)
        t.start()

    def read_data(self):
        """
        reads data coming into the open communication port
        and adds them to te thread-safe queue for data analysis
        """
        data = ''
        while (True):
            new_data = self.serialPort.read()
            if (new_data):
                data += new_data.hex()
                # add the incoming data str to the queue
                if len(data) >= GlobalConstants.MAX_PACKET_LEN:
                    print(data)
                    self.q.put(data)
                    data = ''



#TEST
serial_manager = SerialManager()
serial_manager.print_ports()

#uncomment these when ready to init serial communication
serial_manager.init_connection()
serial_manager.read_data()
