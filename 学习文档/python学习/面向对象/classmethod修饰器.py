'''
    1. @classmethod 是一个装饰器
    2. @classmethod 不需要实例化，不需要带self
    3. 好处在于不需要在修改初始化函数

'''

class My_ClassMethod(object):

    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day
        self.m = 'ytc'
    @classmethod
    def A(cls,str_data):
        y,m,d = map(lambda x: int(x),str_data.split('-'))
        return cls(year=y,month=m,day=d)

    def BL(self):
        # 此时self中的属性均是类修饰方法返回产生
        print(self.year,self.month,self.day)


# 先使用类方法修饰器出一个对象
M = My_ClassMethod.A('2023-12-04')
# 返回的所有属性方法名中包含My_ClassMethod中所有方法
print(M.__dir__())
# 再次调用BL函数方法来生成时间
print(M.BL())





