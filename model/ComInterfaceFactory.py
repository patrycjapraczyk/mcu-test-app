from model.ETHSocketManager import ETHSocketManager
from model.SerialManager import SerialManager
from model.ComErrorStorage import ComErrorStorage


class ComInterfaceFactory:

    @staticmethod
    def get_interface(type, com_error_storage):
        if type == 'ETH':
            return ETHSocketManager()
        elif type == 'SERIAL':
            return SerialManager(com_error_storage)
        else:
            return None

