import socket
import time

HOST = '192.168.3.145'
PORT = 8888
BUFSIZE = 1024
ADD = (HOST, PORT)

socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
socket.connect(ADD)
while 1:
    data = input('>')
    if not data:
        break
    socket.send(str.encode(data))
    data = socket.recv(BUFSIZE)
    data2 = socket.recv(BUFSIZE)
    if not data:
        break
    if not data2:
        break
    print(str(data, encoding='utf-8'))
    print("识别结果为：{}".format(str(data2, encoding='utf-8')))
    print("识别结果的类型为：", type(str(data2, encoding='utf-8')))
socket.close()