import socket
import time

HOST = 'localhost'
PORT = 8888
BUFSIZE = 1024
ADD = (HOST, PORT)

socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
socket.connect(ADD)
while 1:
    data = input('>')
    if not data:
        break
    s = time.time()
    socket.send(str.encode(data))
    print((time.time()-s) * 1000)
    data = socket.recv(BUFSIZE)
    if not data:
        break
    print(str(data, encoding='utf-8'))
socket.close()