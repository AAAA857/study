'''

    __str__ 是python 内置方法，当调用print(obj)将调用__str__

'''

class Base(object):

    def __init__(self):
        self.name = 'abc'

    def Foo(self):
        return '名字叫: %s'%(self.name)

    def __str__(self):
        ''' 调用实例将会返回 Foo()方法 '''
        return self.Foo()

    def __repr__(self):
        print('调用__repr__')

obj = Base()
# 不会调用__str__
print(obj.name)
# 将会调用__str__
print(obj)