import os,sys
sys.path.append('..')
import socketserver
import struct
import subprocess
import platform
import json
import re
from module.secure import auth
from module.Shell import shell

PATH = []
PATH.append(os.path.dirname(os.path.dirname(__file__)))

print('P1',PATH)
'''
    1. Ftpserver需要支持并发访问 ok
    2. 做粘包处理 ok
    2. 支持认证控制 ok
    3. 文件上传
    4. 进度条
    5. 支持执行命令 30%
    6. 支持用户拥有单独的家目录
'''
class MyServer(socketserver.BaseRequestHandler):
    
    action_dict = {
        "action": None,
        "home": None,
        "token": None,
        "user": None,
        "director_size": None,
        "argment": None,
        "status": None
    }
    '''接收字节数'''
    recv_pack_size = 1024
    s = ""
    def __init__(self,*args,**kwargs):
        '''继承父类的__init__不覆盖'''
        super().__init__(*args,**kwargs)
    def Send_Mes(self,mes,first=None):
        if first:
            print('发送struct数据包%s')
            struct_pack = struct.pack('i', len(mes))
            self.request.sendall(struct_pack)
        else:
            self.request.sendall(mes)

    def ls(self,*args):
        '''
            1. 执行ls命令
            2，反射执行对应系统对应ls 执行方法
        '''
        system_type = platform.system()
        hashattr_type = '_ls_{}'.format(system_type.lower())
        if hasattr(self,hashattr_type):
           getattr(self,hashattr_type)(args[0])

    def action_f(self,*args,**kwargs):
        print('执行命令')
        comm = args[0]
        print('comm',comm)
        res = subprocess.Popen(args=comm, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        data = res.stdout.read()
        return data

    def accept_package(self,data):
        number = 0
        s = ""
        print('接收数据',data)
        # 不加会多接受数据
        if data < self.recv_pack_size:
            self.recv_pack_size = data
        else:
            self.recv_pack_size = 1024

        while number < data:
            s += ''.join(self.request.recv(self.recv_pack_size).decode('utf-8'))
            number += self.recv_pack_size
        print('接收完成',s,111)
        return s


    def _get_action(self,data):
        try:
            print('data12',data)
            c_dict = json.loads(data.encode('utf-8'))
            action = c_dict.get('action')
            argument = c_dict
        except ValueError as value_error:
            action = c_dict.get('action')
            argument = ""
        print(action,argument,'测试')
        return action,argument

    def _ls_windows(self,*args):
        a = 'dir {}'.format(args[0].get('argment'))
        res = self.action_f(a)
        self.Send_Mes(mes=res,first=True)
        self.Send_Mes(mes=res)

    def _check_home_dir(self,user):
        '''登录成功用户家目录检测'''
        home_dir = []
        home_dir.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
        home_dir.append('home')
        home_dir.append(user)
        home_path = os.sep.join(home_dir)
        if not os.path.exists(home_path):
            os.mkdir(home_path)
            return os.sep.join([user])
        else:
            return os.sep.join([user])

    def conn(self,*args,**kwargs):
        '''
        `1. 用于client连接验证
         2. 返回client 验证结果
         3. 返回token
         4. 随后的每次连接都要验证token有效性
        :return:
        '''
        print(type(args[0]),args[0])
        c_d = args[0]
        secure_check = auth(username=c_d.get('user'),password=c_d.get('password'))
        status = secure_check.Verify_Password
        print('登录验证')
        self.action_dict['user'] = c_d.get('user')

        if not status:
            self.action_dict['status'] = status

            print('1')
            self.Send_Mes(mes=json.dumps(self.action_dict).encode('utf-8'),first=True)
            self.Send_Mes(mes=json.dumps(self.action_dict).encode('utf-8'))
            print('验证失败断开连接')
            return False

        else:
            self.action_dict['status'] = status[0]
            self.action_dict['token'] = status[1]

            '''判断用户家目录是否存在'''
            user_home = self._check_home_dir(user=c_d.get('user'))
            self.action_dict['home'] = user_home
            print('2',self.action_dict)
            self.Send_Mes(mes=json.dumps(self.action_dict).encode('utf-8'),first=True)
            self.Send_Mes(mes=json.dumps(self.action_dict).encode('utf-8'))
            return True
    def write_or_update(self,mode='wb',totle_size=None,seek=None):

        with open(file=self.action_dict.get('server_file'), mode=mode) as f:
            if seek:
                recv_number = self.action_dict.get('seek_size')
                totle_size -= recv_number
            # try:
            recv_size = 0
            while recv_size < totle_size:
                data = self.request.recv(1024)
                f.write(data)  # 写到内存
                f.flush()  # 刷到硬盘
                recv_size += len(data)
                print('recv_size', recv_size)
        print('写入完成')
        return True
    def write_file(self,update=None):
        print('写入数据开始', self.action_dict,)
        print('写入数据1')

        print('写入数据2')
        totle_size = self.action_dict.get('size')
        if not update:
            self.write_or_update(mode='wb',totle_size=totle_size)
        else:
            self.write_or_update(mode='ab', totle_size=totle_size,seek=True)
        print('写入完成')
        tools = shell()
        # print(self.action_dict.get('server_file'),11000)
        put_status = ('True',tools.file_check_md5(file=self.action_dict.get('server_file'),size=self.action_dict.get('size')))
        # print(put_status)
        # print(('True',tools.file_check_md5(file=self.action_dict.get('server_file'),size=self.action_dict.get('size'))))
        # except Exception as E:
        #     print(E)
        #     put_status = (E)
        # finally:
        '''返回给client报告上传是否完成'''
        '''校验MD5'''
        self.action_dict['put_status'] = put_status
        self.Send_Mes(mes=json.dumps(self.action_dict).encode('utf-8'), first=True)
        self.Send_Mes(mes=json.dumps(self.action_dict).encode('utf-8'))
        del self.action_dict['server_file']
        del self.action_dict['client_file']
        del self.action_dict['put_status']
        return True
    def put(self,data):
        '''
            1. 文件上传功能
            2. 用于进度条
            3. 支持断点续传
        :return:
        '''
        '''获取文件上传文件未知'''
        '''判断本地是否文件存在，并且返回一个消息判断是否进行断点续传'''
        print(
            'put 等待接收第一次数据'
        )
        print(data,1)
        '''断电续传逻辑
            1.新增字典
                self.action_dict['server_file'] = file
                self.action_dict['client_file'] =  argment
                self.action_dict['size'] = 0
        '''
        self.action_dict = self.check_breakpoint(data=data)
        '''
            2. 回复client 数据字典
        '''
        print('put_1', '回复数据包')
        self.Send_Mes(mes=json.dumps(self.action_dict).encode('utf-8'), first=True)
        self.Send_Mes(mes=json.dumps(self.action_dict).encode('utf-8'))
        '''client 发送过来的数据属性字段
            1. 主要获取client 端file size
        '''
        data = struct.unpack('i', self.request.recv(4))[0]
        print('put_2', '获取client 端file size')
        # '''接收数据属性字典'''
        self.action_dict = json.loads(self.accept_package(data=data))

        if self.action_dict.get('put_status') == 'all':
            return self.write_file()
        else:

            # tools = shell()
            print('续传逻辑')
            return self.write_file(update=True)
            # print(('True',tools.file_check_md5(file=r'C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\python学习\socket编程\FTP\home\ytc1\1.txt',size=self.action_dict.get('size')))
    def check_breakpoint(self,data):
        PATH_1 = []
        PATH_1.append(os.path.dirname(os.path.dirname(__file__)))
        print('PATH0', PATH_1)
        PATH_1.append('home')
        PATH_1.append(data.get('home'))
        print('PATH1',PATH_1)
        argment = data.get('argment')
        '''匹配最后一个文件名称'''
        pattern = re.compile(r'^(.*).*(/|\\)(.*)')
        m = pattern.match(argment)
        print(m.group(3),'正则')
        PATH_1.append(m.group(3))
        print('PATH2',PATH_1)
        file = os.sep.join(PATH_1)
        print('file名称',file)
        if not os.path.exists(file):
            '''文件不存在逻辑'''
            self.action_dict['server_file'] = file
            self.action_dict['client_file'] =  argment
            self.action_dict['size'] = 0
        else:
            self.action_dict['server_file'] = file
            self.action_dict['size'] = os.path.getsize(file)
            self.action_dict['client_file'] = argment
        return self.action_dict

    def handle(self):
        while True:
                print('来自%s',self.client_address)
            # 接收第一个数据包，获取对端发送数据包大小
            # try:
                buffer_p = self.request.recv(4)
                if not buffer_p:
                    break
                data = struct.unpack('i',buffer_p)[0]
                accept_data = self.accept_package(data=data)
                '''指令切割'''
                action,argument = self._get_action(data=accept_data)
                print('接收到指令:',action,argument)
                if hasattr(self,action):
                    '''反射调用执行方法'''
                    print('反射执行方法: %s'%(action))
                    getattr(self,action)(argument)
                else:
                    print('没有命令执行通用命令', argument, type(accept_data))
                    res = self.action_f(argument.get('action'))
                    self.Send_Mes(mes=res,first=True)
                    self.Send_Mes(mes=res)

            # except Exception as E:
            #     break

if __name__ == '__main__':

    IP,PORT = ('127.0.0.1',9991)

    s = socketserver.TCPServer(server_address=(IP,PORT),RequestHandlerClass=MyServer)
    s.serve_forever()


