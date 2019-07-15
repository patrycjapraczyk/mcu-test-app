from Data import Data

class DataStorage:
    def __init__(self):
        self.__data_arr = []
        self.curr_data = Data()

    def saveCurrData(self):
        self.__data_arr.append(self.curr_data)
        print(self.curr_data.to_str())
        self.curr_data = Data()

    def printAllData(self):
        for data in self.__data_arr:
            print(data.to_str())