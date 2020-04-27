class StrManipulator:
    @staticmethod
    def substring(data: str, start: int, end: int) -> str:
        """
        :param data: a string to be extracted
        :param start: start index of a string (int)
        :param end: end index of a string (int)
        :return: data[start : end]
        """
        val = data[start: end]
        return val

    @staticmethod
    def remove_every_other(my_list: list, START_FROM_SECOND=False) -> list:
        """
        :param my_list: a list, START_FROM_SECOND - False by default. If True,
                every other element is removed, starting from list[1]
        :return: my_list with every other element removed from it
        """
        return my_list[START_FROM_SECOND::2]

    @staticmethod
    def split_string(data: str, piece_len: int) -> list:
        index_list = []

        end = len(data)
        if end <= 0:
            return index_list

        # split the data string into chunks of length 4
        for i in range(0, end, piece_len):
            data_piece = data[i:i + piece_len]
            index_list.append(data_piece)
        return index_list

    @staticmethod
    def list_into_str(data: list) -> str:
        return ''.join(data)

