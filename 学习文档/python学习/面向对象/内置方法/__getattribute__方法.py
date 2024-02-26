'''
    __getattribute__ 是属性拦截器，默认自带的方法没有执行任何动作，当调用对象属性或方法时都将会调用此方法，当与__getattr__ 一起定义那么
    将不会执行__getarrt__ 只有返回一个AttributeError异常才会调用__getattr__
'''


class Base(object):

    def __init__(self):

        self.name = 'alex'

    def A(self):
        return 'abc'

    def __getattr__(self, item):
        print('---------->')

    def __getattribute__(self, item):
        print('调用__getattribute__ :%s' %(item))
        '''当匹配时将不会调用getattr方法，只有不存在时调用'''
        return object.__getattribute__(self,item)


obj = Base()

print(obj.name)

