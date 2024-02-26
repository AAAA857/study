'''
    特殊属性方法:
        __getattr__ ： 在对象中查找不到对应属性那么将调用此方法  *****
        __setattr__ ： 在对象中设置或更新对应属性那么调用此方法  ***
        __delattr__ :  在对象中删除对应属性那么调用此方法       ***
'''

class Peeple(object):

    def __init__(self,name,age,gender):
        self.name = name
        self.age = age
        self.gender = gender

    def spech(self):
        pass

    def eat(self):
        pass

    '''
        当调用属性在对象中不存在时调用此方法
    '''
    def __getattr__(self, item):
        print('---> 调用__getattr__',item)

    '''
        当设置属性时调用
    '''
    def __setattr__(self, key, value):
        print('--->调用__setattr__',key,value)
        # 如果直接使用字典赋值操作，那么将会报错迭代器溢出
        # 此方式就是调用self 的__setattr__ 所以进入了循环内
        #self.key = value
        # 正确调用方式
        self.__dict__[key] = value

    def __delattr__(self, item):
        print('-->调用__delattr___',item)
        # 与setattr一样 需要对__dict__操作
        del self.__dict__[item]

'''
    需求：
        1. 创建一个class用于做日志操作
        2. 所有实例在写入日志时新增时间戳
'''
import time
class My_Log(object):

    def __init__(self,file_name,model='r+'):
        self.file = file_name
        self.F = open(file=self.file,mode=model,encoding='utf-8')

    '''
        1.  基于类派生功能，修改write方法
        2.  每次写入都将时间戳添加进去
    '''
    def write(self,*args):
        Time = time.strftime('%Y-%m-%d %X')
        info = '%s %s' %(Time,args[0])
        # 写入文件，此处使用self.F write方法
        self.F.write(info)

    ''' 统一方法 '''
    def __getattr__(self, item):
        if hasattr(self.F,item):
            res = getattr(self.F,item)
            return res
        else:
            return '方法不存在'

obj = My_Log(file_name='../info.log', model='a+')
obj.write('abc\n')






