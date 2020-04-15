from model.SerialManager import SerialManager


class MainController:
    def __init__(self):
        self.serial_manager = SerialManager()

    def start_test(self, serial_port, baudrate):
        self.serial_manager.init_connection(serial_port, baudrate)