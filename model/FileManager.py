

class FileManager:
    def __init__(self, FILE_NAME):
        self.FILE_NAME = FILE_NAME
        self.open_file()

    def open_file(self):
        self.f = open(self.FILE_NAME, "w+")

    def file_write(self, msg):
        self.f.write(msg)
        self.f.flush()


