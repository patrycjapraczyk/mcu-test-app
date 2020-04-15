import sys
import glob
import serial

from queue import Queue
from model.DataProcessingThread import DataProcessingThread
from model.GlobalConstants import GlobalConstants


class SerialManager:
    #alter these parameters for your own usecase
    BYTESIZE = 8

    def __init__(self):
        self.q = Queue()
        self.start_data_processing_thread()

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
        return [56000, 115200, 57600, 19200, 9600]


    def init_connection(self, port, baudrate):
        """
        opens a serial communication port
        """
        if port in self.serial_ports():
            self.serialPort = serial.Serial(port, baudrate,
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
#serial_manager = SerialManager()
#serial_manager.print_ports()

#uncomment these when ready to init serial communication
#serial_manager.init_connection()
#serial_manager.read_data()
