'''
    __call__ 方法为python 内置方法，当做对象调用时触发   obj()
'''

class Base(object):

    def __init__(self):
        pass

    def Foo(self,*args,**kwargs):
        return '%s' %(args[0])

    def __call__(self, *args, **kwargs):
        self.Foo(*args,**kwargs)
        print('调用__call__方法')



obj = Base()

print(obj())