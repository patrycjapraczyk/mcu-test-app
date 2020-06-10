from model.Communication.ETHSocketManager import ETHSocketManager
from model.Communication.SerialManager import SerialManager
from model.Interfaces.ComInterface import ComInterface


class ComInterfaceFactory:
    @staticmethod
    def get_interface(type) -> ComInterface:
        if type == 'ETH':
            return ETHSocketManager()
        elif type == 'SERIAL':
            return SerialManager()
        else:
            return None

