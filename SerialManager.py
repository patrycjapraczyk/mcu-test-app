import serial
from queue import Queue
from DataProcessingThread import DataProcessingThread


class SerialManager:
    COM_PORT_NAME = 'COM4'
    BAUDRATE = 9600
    BYTESIZE = 8

    def __init__(self):
        self.q = Queue()

    def init_connection(self):
        self.serialPort = serial.Serial(self.COM_PORT_NAME, self.BAUDRATE,
                                        self.BYTESIZE, serial.PARITY_NONE, serial.STOPBITS_ONE)

    def start_data_processing_thread(self):
        # pass the data to the thread via the queue
        t = DataProcessingThread(self.q)
        t.start()

    def readData(self):
        while (True):
            data = self.serialPort.read()
            if (data):
                data = data.hex()
                print(data)
                # add the incoming data str to the queue
                self.q.put(data)
