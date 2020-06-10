from model.Interfaces.ComInterface import ComInterface
import sys, glob, serial


class SerialManager(ComInterface):
    BYTESIZE = 8
    def __init__(self):
        self.serial_port = None
        self.connected = False

    def init_connection(self, port, baudrate: int):
        """
        opens a serial communication port
        """
        self.serial_port = serial.Serial(port, baudrate,
                                             self.BYTESIZE, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=0)
        if self.serial_port :
            self.connected = True

    def is_connected(self) -> bool:
        return self.connected

    def send_data(self, data: bytearray):
        self.serial_port.write(data)

    def read_data(self) -> bytearray:
        return self.serial_port.read()

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





