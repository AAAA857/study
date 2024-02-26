import socket


def Server_S(*args,**kwargs):
    print(kwargs)
    # 创建一个socket对象
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 为创建的socket对象绑定一个地址
    s.bind((kwargs.get('host'),kwargs.get('port')))

    # 定义socket连接池大小
    s.listen(kwargs.get('bucket_size'))

    # 开始listen
    # 此处循环用于循环accept连接
    while True:
        # accept 将会阻塞住，等待client连接
        # accept 返回俩个连接信息，conn表示client的连接socket对象，addr表示client ip:port信息
        print('开始等待连接')
        conn,addr = s.accept()
        print(addr)

        while True:
            try:
                data = conn.recv(1024)
                # print('收到来自[%s]的一条消息: %s'% (conn,data.decode('utf-8')))

                if not  data: break
                print(data.decode('utf-8'))
                # server 返回消息
                # conn.send(data.upper())
            except Exception as  E:
                break

if __name__ == '__main__':
    print(Server_S(host='127.0.0.1',port=8888,bucket_size=10))