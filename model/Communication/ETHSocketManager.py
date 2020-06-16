import socket
from model.StaticClasses.GlobalConstants import GlobalConstants
from model.Interfaces.ComInterface import ComInterface


class ETHSocketManager(ComInterface):
    def __init__(self):
        self.s = 0
        self.connected = False

    def is_connected(self) -> bool:
        return self.connected

    def init_connection(self) -> None:
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connecting to the data sender
            # TODO: change to use a server configuration listen/accept
            self.s.connect((GlobalConstants.HOST, GlobalConstants.PORT))
            self.connected = True
            print("Socket successfully created")
        except socket.error as err:
            print("socket creation failed with error %s" % err)

    def read_data(self) -> bytearray:
        while True:
            data, addr = self.s.recvfrom(512)  # buffer size is 512 bytes
            return data

    def send_data(self, data: bytearray):
        pass



