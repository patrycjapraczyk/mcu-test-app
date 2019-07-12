import socket
from GlobalConstants import GlobalConstants
from Calculator import Calculator
from DataStorage import DataStorage

calculator = Calculator()
dataStorage = DataStorage()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("socket creation failed with error %s" % (err))

# connecting to the server
s.connect((GlobalConstants.HOST, GlobalConstants.PORT))

def exec():
    while True:
        data, addr = s.recvfrom(512)  # buffer size is 512 bytes
        data = data.hex()
        print(data)
        # if there is some data payload left from the previous iteration
        if dataStorage.curr_data.data_payload:
            if not findEndIndex(data):
                continue
        dataStorage.curr_data.start_index = data.find(GlobalConstants.START_CODE)
        # continue if start_code was not found
        if dataStorage.curr_data.start_index < -1 : continue
        # break if there is errors
        dataStorage.curr_data.err_cnt = calculator.extract(data, dataStorage.curr_data.start_index + GlobalConstants.ERR_CNT_START_INDEX, dataStorage.curr_data.start_index + GlobalConstants.ERR_CNT_END_INDEX)
        if (calculator.getInt(dataStorage.curr_data.err_cnt) > 0):
            raise Exception('ERRORS OCCURED! ', dataStorage.curr_data.err_cnt)

        dataStorage.curr_data.buffer_len = calculator.extract(data, dataStorage.curr_data.start_index + GlobalConstants.BUF_LEN_START_INDEX, dataStorage.curr_data.start_index + GlobalConstants.BUF_LEN_END_INDEX)
        int_len = calculator.getInt(dataStorage.curr_data.buffer_len)
        dataStorage.curr_data.len_of_hex = int_len * 2 - GlobalConstants.START_END_CODE_LENGTH

        findEndIndex(data)


def findEndIndex(data):
    end_index = data.find(GlobalConstants.END_CODE)
    if end_index < 0:
        dataStorage.curr_data_payload += data
        dataStorage.curr_data.start_end_distance = data.length - dataStorage.curr_data.start_index
        return False
    else:
        calcStartEnd(end_index)

        while dataStorage.curr_data.start_end_distance < dataStorage.curr_data.len_of_hex:
            old_end_index = end_index
            end_index = data.find(GlobalConstants.END_CODE, end_index + 1)
            dataStorage.curr_data.start_end_distance += end_index - old_end_index

        # if can't find end code within data length
        if dataStorage.curr_data.start_end_distance > dataStorage.curr_data.len_of_hex:
            raise Exception('MISSING END_CODE!', dataStorage.curr_data.start_end_distance, dataStorage.curr_data.to_str())

        if dataStorage.curr_data.start_index >= 0:
            dataStorage.curr_data.end_index = end_index
            dataStorage.curr_data.data_payload += calculator.extract(data, dataStorage.curr_data.start_index + GlobalConstants.DATA_PAYLOAD_START_INDEX, dataStorage.curr_data.end_index)
            dataStorage.addData()
            dataStorage.printAllData()
            #search for start code message here again
            return True

def calcStartEnd(end_index):
    if dataStorage.curr_data.start_end_distance < 0:
        dataStorage.curr_data.start_end_distance = end_index - dataStorage.curr_data.start_index
    else:
        dataStorage.curr_data.start_end_distance += end_index

exec()