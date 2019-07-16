from Data import Data

class DataStorage:
    def __init__(self):
        self.__data_arr = []
        self.curr_data = Data()

    def saveCurrData(self):
        """"
            adds self.curr_data to self._data_arr
            and clears self.curr_data
        """
        self.__data_arr.append(self.curr_data)
        self.curr_data.payload_len = len(self.curr_data.data_payload)
        print(self.curr_data.to_str())
        self.curr_data = Data()

    def printAllData(self):
        for data in self.__data_arr:
            print(data.to_str())