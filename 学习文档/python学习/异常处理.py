'''
       异常处理：在代码执行过程中会碰见许多未知问题，异常处理就是为了解决此处问题，当发送错误通过异常捕获功能
    来做不通的异常处理动作，python 中异常处理方法try来定义，但是异常处理也不仅仅都是通过try来解决，if之类
    也可以做到，但是try的代码整洁、高效。

        定义格式:
            try:
                pass
            except <error_type> as <alias>:
                pass
            except  .....:
                pass
            else:

                pass
            finally:
                pass
'''
# 使用样例
def test():

    try:
        user_input = input('输入：')
        int(user_input)
    except ValueError as E:
        print('当发送异常被except捕获',E)
    else:
        print('当try没用异常会执行else')
    finally:
        print('不管失败还是成功都会执行finally')


'''
    自定义异常类：
        1. 自定义class需要继承BaseException


'''

class Costom_Error(BaseException):

    def __init__(self,mes):
        self.mes = mes

    def __str__(self):
        return '自定义错误: %s' % self.mes

def Foo():

    try:
        raise Costom_Error('abc')
    except Costom_Error as E:
        print(E)

print(Foo())