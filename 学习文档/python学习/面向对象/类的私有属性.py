'''

    1. python 中没有明确的私有属性方法
    2. python 提供了一种使用规范，定义了某种格式来达成私有属性的一种预定
    3. 私有属性 如同白话，就是一些不想被外部调用的方法或数据属性
    4. 私有属性也是不是滥定义，会让代码看起来不规范

    # 私有属性或私有方法的定义方式
    1. _ 单下划线
    2. __双下划线
        二者均是定义私有属性，但是双下划线会将定义的属性名称做出改变就是重命名
'''
class Money:

    M = {
        "Python": 200,
        "Linux": 220,
        "Java": 180,
        "DBA": 300
    }
    def __init__(self,method):
        self.method = method
    '''
        返回对应工作之外的薪水
    '''
    @property
    def Count_Money(self):
        res = []
        for k,v in self.M.items():
            if self.method == k:
                res.append({k:v})
                break
        return res

class test(object):

    def __init__(self,money,name,method,days):
        self._money = money
        self.name = name
        self.method = method
        self.days = days

    '''定义类方法构建出私有工资属性'''
    @classmethod
    def Get_Mony(clf,O,name,method,days):
        obj = O(method).Count_Money
        return clf(money=obj,name=name,method=method,days=days)

    '''定义计算薪水方法'''
    @property
    def Count_Salary(self):
        self.__salary = int(self._money[0].get(self.method)) * int(self.days)
        return self.__salary

obj = test.Get_Mony(O=Money,name='尹铁城',days='210',method='Python')
print(obj.Count_Salary)
print(obj.__dict__)