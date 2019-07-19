class StrManipulator:
    def extract(data: str, start: int, end: int) -> str:
        """
        :param data: a string to be extracted
        :param start: start index of a string (int)
        :param end: end index of a string (int)
        :return: data[start : end + 1]
        """
        return data[start: end + 1]

    def remove_every_other(my_list: list) -> list:
        """
        :param my_list: a list
        :return: my_list with every other element removed from it
        """
        return my_list[::2]