from model.Communication.CommunicationManager import CommunicationManager
from model.StaticClasses.DataPacketFactory import DataPacketFactory
from model.DataProcessingThread import DataProcessingThread
from model.Data.ComErrorStorage import ComErrorStorage
from model.Data.DataStorage import DataStorage
from model.StaticClasses.GlobalConstants import GlobalConstants
from threading import Thread


class MainController:
    def __init__(self):
        self.com_error_storage = ComErrorStorage()
        self.com_interface = CommunicationManager(self.com_error_storage)
        self.data_storage = DataStorage()
        self.stopped = False

    def start_test(self, serial_port, baudrate):
        self.com_interface.init_connection(serial_port, int(baudrate))
        heartbeat_thread = Thread(target=self.com_interface.heartbeat_loop)
        # pass the data to the thread via the queue
        analysis_thread = DataProcessingThread(self.com_interface.read_data_queue, self.com_error_storage, self.data_storage)
        analysis_thread.attach(self.com_interface)

        analysis_thread.start()
        heartbeat_thread.start()

    def stop_test(self):
        self.stopped = True
        self.com_interface.stop()
        total_packets_received = self.data_storage.data_cnt
        self.com_error_storage.end(total_packets_received)

    def get_correct_percentage(self):
        total_packets = self.data_storage.data_cnt
        return 100 - self.com_error_storage.get_error_percentage(total_packets)

    def get_all_data(self):
        return self.data_storage.data_arr

    def get_heartbeat_periods(self):
        return self.com_interface.heartbeat_period_rates

    def get_ecc_check_periods(self):
        return list(GlobalConstants.ECC_CHECK_PERIODS.keys())

    def send_rest_request(self):
        reset_packet = DataPacketFactory.get_packet('RESET_REQUEST')
        self.com_interface.add_data_to_send_queue(reset_packet)

    def set_heartbeat_period(self, heartbeat_period):
        return self.com_interface.set_heartbeat_period(heartbeat_period)

    def set_ecc_period(self, ecc_check_period):
        return self.com_interface.set_ecc_period(ecc_check_period)

    def get_data(self, data_id):
        return self.data_storage.get_data(data_id)

    def get_com_err(self):
        return self.com_error_storage.com_error_arr

    def get_mem_err_list(self):
        mem_error_storage = self.data_storage.mem_error_storage
        return mem_error_storage.mem_error_arr

    def get_mem_err(self, index):
        mem_error_storage = self.data_storage.mem_error_storage
        return mem_error_storage.get_mem_err(index)

    def get_reset_packets(self):
        reset_storage = self.data_storage.reset_storage
        return reset_storage.reset_arr





