from abc import ABC, abstractmethod


class ComInterface(ABC):
    @abstractmethod
    def init_connection(self) -> None:
        pass

    @abstractmethod
    def read_data(self) -> bytearray:
        pass

    @abstractmethod
    def send_data(self, data: bytearray):
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass