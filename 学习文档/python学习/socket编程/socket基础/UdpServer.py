import socket


def Udp_Server(*args,**kwargs):

    '''
        1. udp 是没连接状态的
        2. udp 不能保证数据的完整性
        3. udp  没三次握手过程
        4. udp  速度快
    '''
    # 获取UDP Socket连接
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    # 绑定UDP端口
    udp_socket.bind((kwargs.get('host'),kwargs.get('port')))

    while True:
        data,addr = udp_socket.recvfrom(1024)
        print(data,addr)

if __name__ == '__main__':

    print(Udp_Server(host='127.0.0.1',port=8888))