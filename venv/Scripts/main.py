import socket

HOST = '192.168.1.100'
PORT = 7771

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("socket creation failed with error %s" % (err))

# connecting to the server
s.connect((HOST,PORT))

while True:
    data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
    print("received message:", data)