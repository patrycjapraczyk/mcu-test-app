class DataStructFunctions:
    @staticmethod
    def chunk(lst: list, n: int):
        """
        chunks a list into slices of length n,
        returns a list of chunks
        """
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @staticmethod
    def get_key(my_dict: dict, value):
        values = list(my_dict.values())
        index = values.index(value)
        keys = list(my_dict.keys())
        return keys[index]
