import socket

HOST = '192.168.1.100'
PORT = 7771

START_CODE = '0xaa'

def checkStart(data):
    start = hex(data[0])
    return start == START_CODE

def getTcpLength(data):
    len = "";
    for x in range (0, 5):
        len += hex(data[x])[2:5]
    return len


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("socket creation failed with error %s" % (err))

# connecting to the server
s.connect((HOST,PORT))

while True:
    data, addr = s.recvfrom(512) # buffer size is 512 bytes
    print(checkStart(data))
    print(getTcpLength(data))
