'''
    __getitem__
    __setitem__
    __delitem__

    三则方法属于内置方法，主要面向于list、dict操作，与attr 系列不同的是 attr 是属性调用使用'.'时才触发，item系列只有在使用切片方法操作时触发


'''
class Base(object):

    def __init__(self):
        self.name = 'alex'

    def __getitem__(self, item):
        print("getitem,args:", item)
        return self.__dict__[item]

    def __setitem__(self, key, value):
        print('setitem',key,value)
        self.__dict__[key] = value

    def __delitem__(self, key):
        print('delattr',key)
        del self.__dict__[key]


obj = Base()



# 将会调用getitem
print(obj['name'])
# 将会调用__setitem__
obj['abc'] = 123
print(obj.__dict__)
del obj['name']
print(obj.__dict__)