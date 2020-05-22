from abc import ABC, abstractmethod


class FileManager(ABC):
    @abstractmethod
    def open_file(self) -> None:
        pass

    def file_write(self, msg) -> bool:
        pass