from ETHSocketManager import ETHSocketManager
from SerialManager import SerialManager

class ComInterfaceFactory:
    def get_interface(self, type):
        if type == 'ETH':
            return ETHSocketManager()
        elif type == 'SERIAL':
            return SerialManager()
        else:
            return None


