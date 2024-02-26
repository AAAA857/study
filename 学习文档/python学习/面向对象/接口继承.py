'''
    接口继承属于面向对象中，类的继承概念，其目的主要是实现一种标准，类似Linux中的概念'一切皆文件'，
 同理python中也是，在python中如果需要这种约束，需要引用第三方模块 abc。
'''
import abc

class Base(metaclass=abc.ABCMeta):

    def __init__(self):
        pass
    '''
        1. 定义接口方法，下面存在俩种方法，read和write，这是一种统一规范，需求就是
        凡是继承了Base类，那么都应改自己定义俩种方法 read 、write
        2. @abc.abstractmethod 首先是一个装饰器，其目的的达成一种约束，如果其他类在
        继承Base类后，那么必须定义了被装饰器 装饰的方法，可以为pass但是必须要求存在
    '''
    @abc.abstractmethod
    def read(self):
        return "read Base"
    @abc.abstractmethod
    def write(self):
        return  "write Base"

class Server1(Base):

    def __init__(self):
        pass
    def read(self):

        return 'From %s read'%(self)

    def write(self):
        return 'From %s write'%(self)

obj = Server1()
print(obj.read())