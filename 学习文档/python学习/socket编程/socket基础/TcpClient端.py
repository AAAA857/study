# -*- coding: utf-8 -*-
import socket
import sys
import time
import struct
import json

recv_size = 1024
d = ""
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',9991))


'''client操作字典'''
action = {
    "action": None,
    "home": None,
    "token": None,
    "user": None,
    "director_size": None,
    "argment": None
}
def client():
    while True:
        action = input('命令:').strip()
        if not  action:continue
        '''发送一个数据包'''

        if action.upper() == 'EXIT':
            client.close()
            break
        send_struct_pack = struct.pack('i',len(action.encode('utf-8')))
        client.sendall(send_struct_pack)
        client.sendall(action.encode('utf-8'))
        res = client.recv(recv_size)
        print(res.decode('gbk'))

if __name__ == '__main__':
    print(len(sys.argv),1111)