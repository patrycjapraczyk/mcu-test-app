from model.ComInterfaceFactory import ComInterfaceFactory
from model.DataPacketFactory import DataPacketFactory

class MainController:
    INTERFACE_TYPE = 'SERIAL'
    def __init__(self):
        self.com_interface = ComInterfaceFactory().get_interface(self.INTERFACE_TYPE)

    def start_test(self, serial_port, baudrate):
        self.com_interface.init_connection(serial_port, baudrate)

    def send_rest_request(self):
        counter = self.com_interface.sent_counter
        reset_packet = DataPacketFactory.get_reset_data(counter)
        self.com_interface.send_data_packet(reset_packet)