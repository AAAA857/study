'''
    迭代器就是重复做一件事，只有调用时才会引用，不会一次性完整的加载到内存中，python中可以迭代类型都
拥有__iter__方法构造而成，并且拥有__next__的对象被称之为迭代器对象，for 就是基于迭代器协议实现方法
当__next__取值为空后会抛出一个异常，for利用异常捕获来终止循环。

    迭代器对象：
        __iter__ 构造方法
        __next__ 获取值方法
'''


# 构建一个迭代器类
class My_Iter_Class(object):

    def __init__(self,number):
        self.number = number

    def __iter__(self):
        '''返回一个迭代器类型'''
        return self

    def __next__(self):
        '''
        :return: 返回 number - 1
        '''
        if self.number == 0:
            raise StopIteration
        self.number -= 1
        return self.number

obj = My_Iter_Class(number=20)

print(obj.__iter__())

for i in obj:
    print(i)