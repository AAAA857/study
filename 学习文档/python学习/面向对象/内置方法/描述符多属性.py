'''

    1.定义属性属性描述符
    2.使用装饰器修饰避免重复代码

'''
class My_Emvellish(object):

    def __init__(self,key,Type):
        self.key = key
        self.type = Type
    def __get__(self, instance, owner):
        return instance.__dict__[self.key]

    def __set__(self, instance, value):
        print('set')
        if not isinstance(value,self.type):
            print('需要使用%s类型'%self.type)
            raise TypeError
        instance.__dict__[self.key] = value

    def __delete__(self, instance):
        del instance.__dict__[self.key]



def A(*args,**kwargs):

    def Inner(fun):

        for k,v in kwargs.items():
            setattr(fun,k,My_Emvellish(key=k,Type=v))
        return fun

    return  Inner


@A(name=str,age=str)
class Foo(object):

    '''重复代码'''
    # name = My_Emvellish(key='name',Type=str)
    # age = My_Emvellish(key='age',Type=int)

    def __init__(self,name,age):
        self.name = name
        self.age = age

    def action(self):
        return  self.name



obj = Foo(name='ytc',age='19')

print(obj.action())





