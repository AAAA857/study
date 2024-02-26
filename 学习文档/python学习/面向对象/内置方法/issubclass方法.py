'''
    issubclass 是python内置方法，用于判断一个类是否为另外一个类的子类

    issubclass(class,typeclass)
        class = 子类
        typeclass = 判断类
'''

class Base(object):
    def __init__(self):
        pass

class Foo(Base):

    def __init__(self):
        pass
# 返回True
print(issubclass(Foo,Base))

