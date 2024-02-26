'''
   importlib 是一个动态根据路径导入模块的方法，可以根据绝对路径和相对路径导入

    方法：
        import_module(name,package) // 需要程序导入的模块名称
            name=模块文件
            package= 如果 name= ./name.py那么需要传入相对路径
        reload(name)    // 热加载对应模块，有时模块更新没有生效，此时需要使用该模块

'''
import  importlib
from 学习目录.python学习.面向对象.test_model.a import test

print(test.Spech('a'))

# 绝对路径方式发哦如test.py文件中的模块
model  = importlib.import_module('test_model.test')
print(model.Spech('b'))

# 相对路径方式导入
model = importlib.import_module(name='.test',package='test_model')
print(model.Spech('c'))

'''在项目中如果存在多个重名模块时使用importlib导入模块更简单'''
# 例如

def Import_Model(name):
    '''
        如果项目中存在多个重复名模块，我们在导入时需要经过判断去引用对应模块，存在代码重复问题
    '''
    if name == 'a':
        from test_model.a import test
    elif name == 'b':
        from test_model.b import  test
    else:
        from test_model.c  import  test
# 使用importlib
def New_Import_Model(path):
    '''
        1.解决代码重复问题
        2.简化代码
    '''
    importlib.reload()
    model = importlib.import_module(name='.test',package=path)
    return model
# 此时在调用模块传入对应的路径即可
model = New_Import_Model('test_model.c')
print(model.Spech('kkk'))