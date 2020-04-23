from model.ETHSocketManager import ETHSocketManager
from model.SerialManager import SerialManager


class ComInterfaceFactory:

    @staticmethod
    def get_interface(type):
        if type == 'ETH':
            return ETHSocketManager()
        elif type == 'SERIAL':
            return SerialManager()
        else:
            return None

