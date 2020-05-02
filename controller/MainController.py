from model.ComInterfaceFactory import ComInterfaceFactory
from model.DataPacketFactory import DataPacketFactory
from model.DataProcessingThread import DataProcessingThread
from model.ComErrorStorage import ComErrorStorage
from model.DataStorage import DataStorage
from model.GlobalConstants import GlobalConstants
from model.Data import Data
from threading import Thread
import time


class MainController:
    INTERFACE_TYPE = 'SERIAL'

    def __init__(self):
        self.com_error_storage = ComErrorStorage()
        self.com_interface = ComInterfaceFactory.get_interface(self.INTERFACE_TYPE, self.com_error_storage)
        self.data_storage = DataStorage()
        data = Data()
        data.complete_data = ''
        #data.complete_data = 'aa001900000000000000000100006666000233330003333381'
        self.data_storage.curr_data = data
        self.data_storage.save_curr_data()

    def start_test(self, serial_port, baudrate):
        self.com_interface.init_connection(serial_port, int(baudrate))
        read_thread = Thread(target=self.com_interface.read_data)
        write_thread = Thread(target=self.com_interface.send_data)
        # pass the data to the thread via the queue
        analysis_thread = DataProcessingThread(self.com_interface.read_data_queue, self.com_error_storage, self.data_storage)
        analysis_thread.attach(self.com_interface)

        time.sleep(2)
        analysis_thread.start()
        read_thread.start()
        write_thread.start()

    def get_all_data(self):
        return self.data_storage.data_arr

    def get_heartbeat_periods(self):
        return self.com_interface.heartbeat_period_rates

    def get_ecc_check_periods(self):
        return list(GlobalConstants.ECC_CHECK_PERIODS.keys())

    def send_rest_request(self):
        counter = self.com_interface.sent_counter
        reset_packet = DataPacketFactory.get_packet('RESET', counter)
        self.com_interface.add_data_to_send_queue(reset_packet)

    def set_heartbeat_period(self, heartbeat_period):
        return self.com_interface.set_heartbeat_period(heartbeat_period)

    def set_ecc_period(self, ecc_check_period):
        return self.com_interface.send_ecc_period_change(ecc_check_period)



