from model.ComInterfaceFactory import ComInterfaceFactory
from model.DataPacketFactory import DataPacketFactory
from model.DataProcessingThread import DataProcessingThread
from model.ComErrorStorage import ComErrorStorage
from threading import Thread
import time


class MainController:
    INTERFACE_TYPE = 'SERIAL'

    def __init__(self):
        self.com_error_storage = ComErrorStorage()
        self.com_interface = ComInterfaceFactory.get_interface(self.INTERFACE_TYPE, self.com_error_storage)

    def start_test(self, serial_port, baudrate):
        self.com_interface.init_connection(serial_port, int(baudrate))
        read_thread = Thread(target=self.com_interface.read_data)
        write_thread = Thread(target=self.com_interface.send_data)
        # pass the data to the thread via the queue
        analysis_thread = DataProcessingThread(self.com_interface.read_data_queue, self.com_error_storage)
        analysis_thread.attach(self.com_interface)

        time.sleep(2)
        analysis_thread.start()
        read_thread.start()
        write_thread.start()

    def send_rest_request(self):
        counter = self.com_interface.sent_counter
        reset_packet = DataPacketFactory.get_packet('RESET', counter)
        self.com_interface.send_data_packet(reset_packet)