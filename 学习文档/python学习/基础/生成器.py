
'''
   可迭代对象： 对象拥有__next__ 方法,可以被__iter__对象初始化

   迭代器: 通过__next__ 方法进行取值当取值空后会抛出一个StopIteration 错误表示迭代对象取空
'''


# t1 = (i for i in range(10))
# print(type(t1))
#
# l = iter([i for i in range(10)])
# while True:
#     try:
#         print(l.__next__())
#     except StopIteration as E:
#         break



'''
    生成器: 生成器用于惰性生成、延迟执行特性，有利于内存节省，生成器取值也是通过迭代器原理实现
'''


# # 生成器方式1
# test01 = (i for i in range(100))
# print(type(test01))
# print(test01.__next__())

# 生成器方式2
def test02(*args):

    for i in range(int(args[0])):
        yield i

res = test02(100)

print(res.__next__())
print(res.__next__())
print(res.__next__())
print(res.__next__())
    

