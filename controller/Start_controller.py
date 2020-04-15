from model.SerialManager import SerialManager

class StartController:
    def get_serial_ports(self):
        return SerialManager.serial_ports()

    def get_baudrates(self):
        return SerialManager.baudrates()