import socket
import struct
import subprocess
import socketserver

class Server(object):

    def __init__(self,ip,port,listen=10):
        self.ip = ip
        self.port = port
        self.s = self.Server_Object()
        self.listen = listen
    def Server_Object(self):
        '''TCP'''
        return socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def __enter__(self):
        print('执行enter')
        self.s = self.Server_Object()
        self.s.bind((self.ip,self.port))
        self.s.listen(self.listen)
        return self.s
    def __exit__(self, exc_type, exc_val, exc_tb):

        self.s.close()

    def action(self,*args,**kwargs):

        comm = args[0]
        print(comm)
        res = subprocess.Popen(args=comm, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        # print(res.stdout.readlines())
        data = res.stdout.read()

        return data

    def Send_Mes(self,c,mes):
        print(mes)
        c.sendall(mes)

if __name__ == '__main__':

    obj = Server(ip='127.0.0.1',port=8889)

    with obj as s:
        while True:
            print('TCP开始监听')
            client_socket,client_address = s.accept()

            print(client_address)

            while True:
                '''接收数据'''
                try:

                    data = client_socket.recv(1024)
                    if not data:
                        break
                    res = obj.action(data.decode('utf-8'))
                    print(res.decode('gbk'))
                    struct_pack = struct.pack('i',len(res))
                    obj.Send_Mes(c=client_socket,mes=struct_pack)

                    obj.Send_Mes(c=client_socket,mes=res)
                except Exception as E:
                    client_socket.close()
                    break