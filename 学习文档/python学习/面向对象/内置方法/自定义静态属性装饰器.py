class My_Descriptor(object):

    def __init__(self,fun):
        self.fun = fun

    def __get__(self, instance, owner):
        print('get')
        if instance is None:
            return self
        return  self.fun(instance)

    def __set__(self, instance, value):
        print('set')

    def __delete__(self, instance):
        pass

class Foo(object):

    def __init__(self,g,h):
        self.long = g
        self.high = h

    @My_Descriptor
    def action(self):
        return self.long * self.high

# obj = Foo(100,100)
# print(obj.action)


print(Foo.action)