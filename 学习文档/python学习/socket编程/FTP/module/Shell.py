import  os
import sys
import  subprocess
import hashlib
import platform
'''
    定义ftp支持执行的bash语句
'''

def run_shell(*args):
    print('执行命令')
    comm = args[0]
    print('comm', comm)
    res = subprocess.Popen(args=comm, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    data = res.stdout.read()
    return data

class shell(object):

    def __init__(self):
        pass


    def cd(self):

        pass

    def mkdir(self):

        pass

    def rm(self):

        pass


    def file_check_md5(self,file,size):

        '''
        :param data: 接收文件
        :return: 返回校验结果
        '''
        # print(file,size,'shell')
        with open(file=file,mode='rb') as r :
            '''实例化hashlib.md5'''
            md5 = hashlib.md5()
            number = 0
            recv_size = 1024

            total_size = size
            while number < size:
                if total_size < recv_size:
                    recv_size = recv_size - total_size
                    md5.update(r.read(recv_size))
                else:
                    md5.update(r.read(recv_size))
                number += recv_size
                total_size -= size
            print(md5.hexdigest())

            return md5.hexdigest()


if __name__ == '__main__':

    obj = shell()
    file = r'/学习目录/python学习/socket编程/FTP/home/ytc1/logstash-7.17.8-linux-x86_64.tar.gz'
    file1 = r'C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\python学习\socket编程\FTP\bin\1.txt'
    size = os.path.getsize(filename=file)
    size1 = os.path.getsize(filename=file1)

    print(obj.file_check_md5(file=file,size=size))
    # print(obj.file_check_md5(file=file1, size=size1))