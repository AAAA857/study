import os
import stat
import time
# path 模块
''' 
    path.join 用于拼接路径，会根据操作系统自动选择使用那种拼接符号
'''
print(os.path.join('a','b'))
'''
    path.dirname 拥有返回一个文件的父级目录
    注：
        在pycharm中使用__file__会帮忙拼接完整目录
        如果非pycharm环境使用应该加上abs绝对路径
'''
print(os.path.dirname(__file__))
print(os.path.dirname(os.path.abspath(__file__)))

'''
    path.split 用于切割路径，返回一个元组、元素为路径 + 文件名称
'''
print(os.path.split(os.path.abspath(__file__)))

'''
    path.basename 返回文件名称
'''
print(os.path.basename(__file__))


'''
    path.commonpath 接受一个列表，列表里面保存绝对路径，它的作用是帮忙获取最长相同共有的路径
'''
l = ['/home/User/Photos', '/home/User/Videos']
print(os.path.commonpath(l))
print(os.path.commonprefix(l))


'''
    path.exists  接受一个路径， 用于判断是否存在
        retunt: True 或 False
'''
print(os.path.exists(__file__))
'''
    path。expanduser 用于将~线换成用户的主目录路径
'''
print(os.path.expanduser('~/a/b/c'))
print(os.path.expandvars('~/a/b/c'))

'''  
    用于获取文件时间属性：
    path.getatime   文件访问时间 
    path.getctime   文件创建时间
    path.getmtime   文件修改时间
'''
print(os.path.getatime(__file__))
print(os.path.getmtime(__file__))
print(os.path.getctime(__file__))

'''
    path.isabs 用来判断是否为绝对路径
'''
print(os.path.isabs(__file__))
print(os.path.isabs('a.txt'))

'''

    path.getsize    返回文件大小
'''
print(os.path.getsize(__file__))

'''
    path.isdir  用来判断是否为一个目录
'''
print(os.path.isdir(__file__))

'''
    path.sep 用来生成对于系统的拼接符号
'''
print(os.path.sep)
l = ['a','b','c']
res = os.path.sep.join(l)
print(res)

print(os.path.realpath(__file__))
print(os.path.relpath(__file__,start='/'))

'''
    os.stat  获取文件属性信息
'''
# print(os.stat(__file__))
#
# print(os.chdir(os.getcwd()))
# print(os.chmod(__file__,mode=stat.S_IXOTH))
# print(os.stat(__file__))
# print(os.chroot(__file__))

'''
    os.getpid   获取进程id
    os.getppid  获取父进程id
'''
print(os.getpid(),os.getppid())

'''
    获取目录下面所有文件，返回列表
'''
# print(os.listdir(os.path.dirname(__file__)))
# path = 'abc'
# print(os.mkdir(path=path))

r,w = os.pipe()
res = os.fork()
if res:

    print('1')
else:
    print('2')