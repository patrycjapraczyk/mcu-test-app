import socket
from queue import Queue

from model.DataProcessingThread import DataProcessingThread
from model.GlobalConstants import GlobalConstants


class ETHSocketManager:
    def __init__(self):
        self.q = Queue()
        self.messages = []
        self.open_socket()
        self.start_data_processing_thread()
        self.receive_data()

    def open_socket(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket successfully created")
        except socket.error as err:
            print("socket creation failed with error %s" % err)

        # connecting to the data sender
        self.s.connect((GlobalConstants.HOST, GlobalConstants.PORT))

    def start_data_processing_thread(self):
        # pass the data to the thread via the queue
        t = DataProcessingThread(self.q)
        t.start()

    def receive_data(self):
        while True:
            data, addr = self.s.recvfrom(512)  # buffer size is 512 bytes
            data = data.hex()
            # add the incoming data str to the queue
            self.q.put(data)

