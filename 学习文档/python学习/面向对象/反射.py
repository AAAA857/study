'''
    反射：
        1. 通过字符串的方式去检查我们的方法是否存在
        2. 通过字符串的方式去调用我们的方法

    反射常用方法:
        getattr()   // 获取
        setattr()   // 修改
        hasattr()   // 判断
        delattr()   // 删除
'''

# getattr()
# setattr()
# hasattr()
'''例子'''
class People(object):
    # 实例属性
    def __init__(self,name,age,gender):
        self.name = name
        self.age = age
        self.gender = gender

    def spech(self,words):
        mes = '%s spech %s' %(self.name,words)
        return mes
    def info(self):
        return '性别: %s,姓名: %s'%(self.gender,self.name)


# 判断People类中是否存在spech方法
# 当存在时那么返回True，不存在返回False
res = hasattr(People,'spech')   #True
res = hasattr(People,'kkkk')    #False
print(res)
# 调用People中姓名
obj = People('尹铁城','18','男')
res = getattr(obj,'name')   # 获取到name实例属性
print(res)

# 新增实例中一个属性
setattr(obj,'hobby','NBA')
print(obj.__dict__)
res = getattr(obj,'hobby')
print(res)


''' 
    使用案例：
        1. 接受用户输入的方法
        2. 如果方法存在执行对应模块，不存在返回模块不存在 

'''
obj = People('尹铁城','18','男')
M = input('输入方法名称:')

if hasattr(obj,M):
    res = getattr(obj,M)
    print(res())
else:
    print('模块不存在')
