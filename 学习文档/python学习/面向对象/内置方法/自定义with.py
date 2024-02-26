'''
    有写任务中需要先做设置，随后执行完成后需要做事后清理 with就是做这个事情的，
其中with 预设值执行的是__enter__内置方法，执行结束后需要执行__exit__方法做
任务结束清理，__exit__接收有俩种标准，其一是with代码块执行完成，其二是遇见异常
错误。

    自定义方法:
        __enter__: whit 语句调用时触发此方法
        __exit__： 任务结束时触发
'''

# 自定义whit类
class My_Whit(object):
    def __init__(self,number):
        self.number = number

    def __enter__(self):
        print('调用了enter方法')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        print('任务结束了')

    def __iter__(self):
        return self

    def __next__(self):
        if self.number == 0:
            raise StopIteration
        else:
            self.number -= 1
            return self.number


if __name__ == '__main__':
    # m=self
    with My_Whit(number=20) as m:
        print(m.__next__())
        print(m.__next__())