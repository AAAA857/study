'''
    类的静态属性:
        1. 使用staticmethod 模块定义
        2. 脱离实例、脱离类
        3. 属于类的工具库
        4. 静态方法就是类对外部函数的封装，有助于优化代码结构和提高程序的可读性。

'''



class My_Static(object):


    def __init__(self):
        print('类实例化')
        self.name = 'ytc'

    # 声明一个静态方法
    @staticmethod
    def Mstatic_Methon(a,b,c):
        # 此时将无法调用class中的任何数据属性和函数方法
        #print(self.name)
        return  a,b,c






#

print(My_Static.Mstatic_Methon(1,2,3))