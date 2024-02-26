# -*- coding: utf-8 -*-

import socket
import sys
sys.path.append('..')
import time
import struct
import json
import os
import hmac
from module.Shell import shell

class Ftp_Client(object):
    '''client操作字典'''
    action_dict = {
        "action": None,
        "home": None,
        "token": None,
        "user": None,
        "director_size": None,
        "argment": None
    }
    def __init__(self,user,password,ip,port):
        self.user = user
        self.password = password
        self.ip = ip
        self.port = int(port)
        self.recv_size = 1024

    def conn(self):
        '''建立socket连接'''
        self.client.connect()
        return s

    def auth_check(self):
        '''
            1. 验证账号密码有效性
            2. 如果验证成功记录token到字段中
            3. 验证成功进入到C_Shell终端进行后续操作
            4. 验证失败退出
        '''

        self.action_dict['user'] = self.user
        self.action_dict['password'] = self.password
        self.action_dict['action'] = "conn"

        self.Send_Message_Json(self.action_dict,frist=True)

        first_pack = struct.unpack('i',self.client.recv(4))
        s = self.Recv_Package(mes=first_pack,decode='utf-8')
        self.action_dict = json.loads(s)
        print(type(self.action_dict),self.action_dict)
        return self.action_dict

    def stuct_pack(self,mes):

        return struct.pack('i',len(json.dumps(mes).encode('utf-8')))

    def Recv_Package(self,mes,decode='utf-8'):
        print('第一个包是%s' % mes, type(mes))
        package_totle_a = 0
        s = ""
        while package_totle_a < mes[0]:
            s += ''.join(self.client.recv(self.recv_size).decode(decode))
            package_totle_a += self.recv_size
        return s

    def Send_Message_Json(self,mes,frist=None):
        if frist:
            # send_struct_pack = struct.pack('i', len(json.dumps(self.action_dict).encode('utf-8')))
            send_struct_pack = self.stuct_pack(mes)
            print('发送了第一个包')
            self.client.sendall(send_struct_pack)
            self.client.sendall(json.dumps(self.action_dict).encode('utf-8'))
            print('发送完成',json.dumps(self.action_dict).encode('utf-8'))
        else:
            self.client.sendall(json.dumps(self.action_dict).encode('utf-8'))

    def Universal_Method(self,mes):
        print('mes',mes)
        self.Send_Message_Json(mes=mes, frist=True)
        # self.Send_Message_Json(mes=mes)
        first_pack_v = struct.unpack('i', self.client.recv(4))
        res = self.Recv_Package(mes=first_pack_v)
        return res
    #定义一个进度条
    def process_bar(self,num, total):
        '''
        :param num: 等于上传大小
        :param total: 等于总大小
        :return:
        '''
        rate = float(num)/total
        ratenum = int(100*rate)
        r = '\r[{}{}]{}%'.format('*'*ratenum,' '*(100-ratenum), ratenum)
        sys.stdout.write(r)
        sys.stdout.flush()
    def vrify_file(self,resp,local_file_size):
        '''本地校验md5'''
        tools = shell()
        vrify_md5 = tools.file_check_md5(
            file=self.action_dict.get('client_file'),
            size=local_file_size
        )
        print('开始本地校验: %s,%s,%s'%(vrify_md5,resp,self.action_dict.get('client_file')))
        status = hmac.compare_digest(vrify_md5,resp)
        if status:
            return '文件发送完成!'
        else:
            return '校验md5失败!'
    def total_put(self,local_file_size,update=None,seek_size=None):
        '''进入发送文件内容逻辑，字节方式发送'''
        with open(file=self.action_dict.get('client_file'), mode='rb') as r:
            increase_number = 0
            send_size = 4096
            print('put 2 ')
            if not update:
                while increase_number < local_file_size:
                    self.client.send(r.read(send_size))
                    increase_number += send_size
                    '''进度条'''
                    self.process_bar(num=increase_number, total=local_file_size)
            else:
                r.seek(seek_size)
                increase_number = seek_size
                while increase_number < local_file_size:
                    self.client.send(r.read(send_size))
                    increase_number += send_size
                    '''进度条'''
                    self.process_bar(num=increase_number, total=local_file_size)
        # 接收server上传完成确认
        struct_unpack = struct.unpack('i', self.client.recv(4))
        resp = json.loads(self.Recv_Package(mes=struct_unpack))
        if resp.get('put_status')[0]:
            '''本地校验md5'''
            res =self.vrify_file(resp=resp.get('put_status')[1],local_file_size=local_file_size)
            return res
        else:
            return resp
    def put(self,mes):
        print('c_put 1 ',mes)
        # self.action_dict = json.loads(self.Universal_Method(mes=mes))
        # 发送第一条消息 server 去执行put 动作
        self.Send_Message_Json(mes=mes,frist=True)
        # server侧进入put方法
        '''
            server侧相应数据包
                1. 第一次粘包处理
                2. 进行循环接收数据包
    '''
        # struct_unpack = 元组(size)
        struct_unpack = struct.unpack('i',self.client.recv(4))
        #  接收数据字典
        self.action_dict = json.loads(self.Recv_Package(mes=struct_unpack))
        print('c_put 2 ',self.action_dict)
        try:
            # 获取server 返回的数据属性字典，获取本地上传文件
            local_file_size =  os.path.getsize(self.action_dict.get('client_file'))
            print('c_put 3',local_file_size)
        except Exception as E:
            print('上传文件不存在!')
            return False
        '''0 表示不需要断点续传直接上传即可'''
        if self.action_dict.get('size') == 0:
            print('c_put 4 ')
            '''发送json数据新增需要上传的文件大小'''
            if not os.path.isfile(self.action_dict.get('client_file')):
                '''
                上传非文件为一个目录
                1. 补充方法循环将目录下面所有文件全部上传
                '''
                pass
            else:
                print('c_put 5 ')
                '''
                 文件上传逻辑
                    1. 发送文件大小   ok
                    2. 进入循环       ok
                    3. 用于进度条      
                '''
                '''修改属性字典覆盖server返回的size大小，因为已经没有意义'''
                self.action_dict['size'] = local_file_size
                self.action_dict['put_status'] = 'all'
                # 发送本地文件大小 server做读取
                self.Send_Message_Json(mes=self.action_dict,frist=True)
                return self.total_put(local_file_size=local_file_size)
        else:
            '''断点续传
                1. 读取文件应该seek到server返回的size大小
                2. md5校验逻辑，判断返回的是否与本地的文件相同
                3. md5一致将不上传
            '''
            # 获取server 端已经上传文件大小
            server_upload_size = self.action_dict.get('size')
            # 本地文件大小
            self.action_dict['seek_size'] = self.action_dict.get('size')
            self.action_dict['size'] = local_file_size
            self.action_dict['put_status'] = 'update'
            # 发送本地文件大小 server做读取
            self.Send_Message_Json(mes=self.action_dict, frist=True)
            # seek 然后直接发送

            # 配合进度条
            return self.total_put(local_file_size=local_file_size,update=True,seek_size=server_upload_size)



    def ls(self,mes):
        res = self.Universal_Method(mes=mes)
        return res

    def C_Shell(self,status):

        while True:
            if not status.get('status'):
                self.client.close()
                return
            self.action_dict['action'] = None
            action = input('%s:'%(status.get('home'))).strip().split(sep=' ')
            if  action[0] == '':
                continue
            '''发送一个数据包'''
            if action[0].upper() == 'EXIT':
                self.client.close()
                break
            self.action_dict['action'] = action[0]
            try:
                self.action_dict['argment'] = action[1]
            except IndexError as  I:
                self.action_dict['argment'] = ''
            '''反射调用client端方法'''
            print(action,'执行方法')
            if hasattr(self,action[0]):
                res = getattr(self,action[0])(self.action_dict)
                print(res)
            else:
                res = self.Universal_Method(mes=self.action_dict)
                print(res)
    def __call__(self, *args, **kwargs):
        print('运行了__call__')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('10.180.0.56',9992))
        '''返回状态字段'''
        status = self.auth_check()
        if not status.get('status'):
            return '认证失败!'
        self.C_Shell(status)

if __name__ == '__main__':
    a, i, P, u, p = 'conn','10.180.0.56',9991,'ytc1','1234567'
    # a,i,P,u,p = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]
    if a == 'conn':
        s = Ftp_Client(user=u,password=p,ip=i,port=P)
        print(s())
    else:
        print('需要先连接到server!')