'''
    python 中描述的作用是用来代理其他类的类属性，白话来讲就是在代理的类中，如果调用了代理的类属性，那么将
会触发文件描述类中的对应方法，其方法有__get__、__set__、__delete__方法.
    描述符可以用来控制对属性的访问行为，实现计算属性、懒加载属性、属性访问控制等功能，

    方法：
        __get__         查询时触发
        __set__         修改时触发
        __delete__      删除时触发

    类型：
        数据描述符:      描述符类中必须拥有__get__、__set__两种方法
        非数据描述符:     描述符类中没有定义__set__方法

    优先级：  所谓的优先级就是查询或定义匹配次序
        类属性 > 数据描述符合 > 实例属性 > 非数据描述符

'''

'''
    1. 定义一个描述符类
    2. 控制age只允许使用int方式定义
'''
# class Proxy_Age(object):
#
#     '''init 方法接收一个需要代理的类属性名称'''
#     def __init__(self,key):
#         self.key = key
#     '''
#         1. 当只定义了一个__get__或与__delete__一起定义没有定义__set__ 那么这个描述符属于非数据描述符
#     '''
#     def __get__(self, instance, owner):
#         # instance 代表实例化对象
#         # owner    代表类名称
#         print('触发描述符get方法')
#         '''get 查询时触发，因此需要返回查询结果'''
#         return  instance.__dict__[self.key]


class Proxy_Age(object):

    '''init 方法接收一个需要代理的类属性名称'''
    def __init__(self,key):
        self.key = key
    '''
        1. 定义__set__方法将会变成数据描述符
    '''
    def __get__(self, instance, owner):
        # instance 代表实例化对象
        # owner    代表类名称
        print('触发描述符get方法')
        '''get 查询时触发，因此需要返回查询结果'''
        return  instance.__dict__[self.key]
    def __set__(self, instance, value):
        # instance 代表实例对象
        # value     代表设置的值
        print('调用描述符的set方法')
        '''实例的属性都保存在自己的属性字典中'''

        if isinstance(value,int):
            instance.__dict__[self.key] = value
        else:
            print('%s 只允许为int类型'% self.key)


    def __delete__(self, instance):
        print('调用描述符delete方法')
        '''实例的属性都保存在自己的属性字典中'''
        instance.__dict__[self.key].pop()

#
class Foo(object):
    # 定义描述符代理
    age = Proxy_Age(key='age')
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def Action(self):
        return '名字:[%s] 年龄:[%s]' %(self.name,self.age)

# 此时调用将触发描述符，因为优先级原因
# 此时的age将不允许使用非int类型方式去做定义
obj = Foo(name='alex',age='19')
print(obj.Action())


