from abc import ABC, abstractmethod


class ComInterface(ABC):
    @abstractmethod
    def init_connection(self) -> None:
        pass

    @abstractmethod
    def read_data(self) -> None:
        pass

    @abstractmethod
    def add_data_to_send_queue(self, data: bytearray) -> None:
        pass

    @abstractmethod
    def send_data_packet(self, data: bytearray):
        pass

    @staticmethod
    def get_max_frames_num(period, baudrate) -> int:
        pass

    @abstractmethod
    def send_packet_stream(self) -> None:
        pass