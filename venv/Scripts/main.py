import socket
from queue import Queue
from threading import Thread
from GlobalConstants import GlobalConstants
from DataProcessingThread import DataProcessingThread

class DataStreamer:
    def __init__(self):
        self.q = Queue()
        self.openSocket()
        self.startDataProcessingThread()
        self.receiveData()

    def openSocket(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket successfully created")
        except socket.error as err:
            print("socket creation failed with error %s" % (err))

        # connecting to the data sender
        self.s.connect((GlobalConstants.HOST, GlobalConstants.PORT))

    def startDataProcessingThread(self):
        t = DataProcessingThread(self.q)
        t.start()

    def receiveData(self):
        self.startDataProcessingThread()
        while True:
            data, addr = self.s.recvfrom(512)  # buffer size is 512 bytes
            data = data.hex()
            # add the incoming data str to the queue
            self.q.put(data)


dataStreamer = DataStreamer()