from threading import Thread
from queue import Queue

class DataProcessingThread(Thread):
    def __init__(self, queue: Queue):
        Thread.__init__(self)
        self.q = queue

    def run(self):
        while True:
            data_item = self.q.get()
            print(data_item)