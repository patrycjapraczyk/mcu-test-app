class DataStructFunctions:
    @staticmethod
    def chunk(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @staticmethod
    def get_key(my_dict: dict, value):
        values = list(my_dict.values())
        index = values.index(value)
        keys = list(my_dict.keys())
        return keys[index]
