import socket
import time
class Server(object):

    def __init__(self,ip,port,listen=5):


        self.ip = ip
        self.port = port
        self.s = self.Socket_Server()
        self.listen = listen
    def Socket_Server(self):
        return socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def Bind_Server(self):
        self.s.bind((self.ip,self.port))
        return self.s

    def __call__(self, *args, **kwargs):

        s = self.Bind_Server()
        print('开始监听')
        while True:
            data, addr = s.recvfrom(1024)
            if data.decode() == 'time':
                T = time.strftime('%Y-%m-%d %X')
                s.sendto(T.encode('utf-8'),addr)

if __name__ == '__main__':

    obj = Server('127.0.0.1',8888)
    obj()


