import socket
import time

'''
SOCKET服务端建立
1.创建一个socket
2.绑定IP地址与端口
3.开启监听
4.开启接受客户端的连接
5.收发数据，send(), recv() {一般来说收数据的时候需要验证数据的完整性，可通过1.基础数据接收法 2.尾标识方法 3.负载长度方法}
6.关闭
'''


HOST = 'localhost'
PORT = 8888
BUFZISE = 1024
ADDR = (HOST, PORT)

# 建立socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定host与端口
socket.bind(ADDR)

'''
两层while循环，第二层接收数据，如果客户端断开连接，
则跳出第二层循环，返回第一层循环：等待连接
'''
while 1:
    # 监听
    socket.listen(5)
    print("waiting for connection..")
    # 接受客户端的连接
    socket_acc, addr = socket.accept()
    print("..connected from", addr)
    while 1:
        # 接受数据
        try:
            data = socket_acc.recv(BUFZISE)
        except Exception:
            break
        data = str(data, encoding='utf-8')
        print(data)
        # 发送数据
        socket_acc.send(str.encode('[%s]%s' % (time.ctime(), data)))

