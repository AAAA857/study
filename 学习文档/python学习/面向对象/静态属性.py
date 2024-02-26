'''
    1. @property 定义静态属性
    2. 静态属性的好处方式属性被修改，因为是将一个函数方法定义成了属性
    3. 不在使用函数调用方式来运行，转化为调用属性方式执行
    4. 静态属性是只读的不可以进行修改
    5. 定义为静态属性的方法可以调用实例自己和类共有的数据属性、方法
'''


class My_Property(object):

    def __init__(self):
        self.name = 'ytc'
    # 定义静态属性
    @property
    def test(self):
        return self.name

My_Object = My_Property()

print(My_Object.__dict__)
print(My_Object.test)
# 下面属性修改将会发生错误
#My_Object.test = '123'
# 下面实例数据属性修改不会返回异常
My_Object.name = '1234'
print(My_Object.name)
