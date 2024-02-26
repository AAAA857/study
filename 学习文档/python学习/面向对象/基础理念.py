'''
什么是类:
    1. 首先python使用class定义类
    2. 类是一类共同特性的集合
    3. 类用于数据属性、函数方法

什么是方法：
    1. 类方法实际是函数的封装
    2. 实例化后用户可以调用类方法
    3. 对应每个方法都是类里面封装的一个功能模块

什么是面向对象：
    1. python中面向对象是一种编程范式
    2. 封装、继承、多态 特性

什么是实例:
    1. 实例的生成是需要先做实例化的一个过程
    2. 每个实例都用于自己的数据属性
    3. 继承 类中的方法，可以调用类中数据属性
'''

# 类语法
'''
    class 用于俩种定义形态:
        1. 新式类： 
            1.1： 每个类名都应包含参数object，继承概念
        2. 原始类
            2.1:  每个类不需要定义参数
'''
class My_Class(object):

    # __init__ 是一个初始化函数
    # 每个实例自己的数据属性
    def __init__(self,name,age):

        self.name = name
        self.age = age
        print('每次实例化都会执行__init__初始化函数')

    def test(self):
        return self.name



# 实例化
My_Object = My_Class(name='ytc',age=18)

# 返回当前实例属性字典
print(My_Object.__dict__)
print(My_Class.__dict__)
res = My_Object.test()
print(res)