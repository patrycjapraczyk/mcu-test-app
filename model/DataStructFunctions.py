class DataStructFunctions:
    @staticmethod
    def chunk(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @staticmethod
    def get_key(my_dict: dict, value):
        my_dict.keys()[my_dict.values().index(value)]
