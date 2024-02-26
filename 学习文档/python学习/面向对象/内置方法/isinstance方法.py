'''

    isinstance() 是python 内置方法，用于判断一个对象是否的指定类或元组中任意一个类实例

        isinstance（object，classinfo）
            object=要检查的对象
            classinfo=判断的类或元组


'''

class Base(object):

    def __init__(self):
        self.name = 'abc'
        
obj = Base()

print(isinstance(obj,Base))