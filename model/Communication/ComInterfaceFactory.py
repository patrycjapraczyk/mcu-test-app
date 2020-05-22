from model.Communication.ETHSocketManager import ETHSocketManager
from model.Communication.SerialManager import SerialManager


class ComInterfaceFactory:
    @staticmethod
    def get_interface(type, com_error_storage):
        if type == 'ETH':
            return ETHSocketManager()
        elif type == 'SERIAL':
            return SerialManager(com_error_storage)
        else:
            return None

